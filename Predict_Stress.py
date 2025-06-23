import torch
import numpy as np
import joblib  
import torch.nn as nn

class ProtoNet(nn.Module):
    def __init__(self, feature_dim=1024):
        super(ProtoNet, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(4, 4096),
            nn.ReLU(),
            nn.BatchNorm1d(4096, track_running_stats=False),
            nn.Dropout(0.3),
            nn.Linear(4096, 2048),
            nn.ReLU(),
            nn.BatchNorm1d(2048, track_running_stats=False),
            nn.Dropout(0.3),
            nn.Linear(2048, feature_dim),  # Ensure this is the final embedding size
            nn.ReLU(),
            nn.BatchNorm1d(feature_dim, track_running_stats=False)
        )

    def forward(self, x):
        if self.training or x.shape[0] > 1:  # Normal forward for batches
            return self.encoder(x)
        else:
            # Handle single sample inference correctly (skip BatchNorm issues)
            for layer in self.encoder:
                if isinstance(layer, nn.BatchNorm1d):
                    continue  # Skip BatchNorm for single input
                x = layer(x)
            return x  # Return correctly shaped embedding


# Load Model
device = "cuda" if torch.cuda.is_available() else "cpu"
protonet = ProtoNet().to(device)
protonet.load_state_dict(torch.load("best_protonet_model.pth", map_location=device))
protonet.eval()

# Load Training Data and Scaler
X_train = np.load("X_train.npy")
y_train = np.load("y_train.npy")
scaler = joblib.load("scaler.pkl")  # Load the scaler saved in Colab

# Define the function to make predictions
def predict_stress(sys_bp, dia_bp, heart_rate, spo2):
    input_data = np.array([[sys_bp, dia_bp, heart_rate, spo2]])
    input_data_scaled = scaler.transform(input_data)  # Scale input
    
    input_tensor = torch.tensor(input_data_scaled, dtype=torch.float32).to(device)

    # Compute class prototypes
    def euclidean_distance(a, b):
        return torch.cdist(a, b, p=2)

    with torch.no_grad():
        embedding = protonet(input_tensor)
        class_prototypes = torch.stack([
            protonet(torch.tensor(X_train[y_train == i], dtype=torch.float32).to(device)).mean(0)
            for i in np.unique(y_train)
        ])
        dists = euclidean_distance(embedding, class_prototypes)
        pred_label = torch.argmin(dists, dim=1).item()

    # Map label to class
    label_map = {0: "Normal", 1: "Stress High"}
    return label_map[pred_label]