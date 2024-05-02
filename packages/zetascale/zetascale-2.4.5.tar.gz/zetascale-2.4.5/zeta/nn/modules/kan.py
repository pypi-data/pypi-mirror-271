import torch
import torch.nn as nn
import torch.nn.init as init
from torch import Tensor, nn


class BSplineBasis(nn.Module):
    def __init__(self, order, num_basis):
        super(BSplineBasis, self).__init__()
        self.order = order
        self.num_basis = num_basis
        # Adding 'order - 1' ensures there are enough control points
        self.control_points = nn.Parameter(torch.linspace(0, 1, steps=num_basis + order - 1), requires_grad=False)

    def forward(self, x):
        # Ensure x is within [0, 1]
        x = x.unsqueeze(-1)  # Expand dims for broadcasting, now shape [N, 1]
        control_points = self.control_points.unsqueeze(0)  # Shape [1, num_points]

        # Create masks for interval inclusion
        left = control_points[:, :-1]  # Removing the last point
        right = control_points[:, 1:]  # Removing the first point

        # Calculate basis functions starting with zeroth order
        N = torch.zeros(x.shape[0], self.num_basis + self.order - 2, device=x.device)
        within_bounds = (x >= left) & (x < right)
        N[within_bounds] = 1

        # Recursive calculation of B-spline basis of higher orders
        for d in range(2, self.order + 1):
            N_left = (x - left[:, :-(d-1)]) / (right[:, :-(d-1)] - left[:, :-(d-1)]) * N[:, :-(d-1)]
            N_right = (right[:, d-1:] - x) / (right[:, d-1:] - left[:, d-1:]) * N[:, 1:-d+2]
            N = N_left + N_right

        return N
    
class KAN(nn.Module):
    def __init__(
        self,
        dim: int,
        depth: int,
        alpha: float = 1.0,
        num_splines: int = 10,
        spline_order: int = 3
    ):
        super(KAN, self).__init__()
        self.dim = dim
        self.depth = depth
        self.alpha = alpha
        self.spline_order = spline_order
        self.num_splines = num_splines

        # Initialize the Activation
        self.soft = nn.Softplus()
        self.w = nn.Parameter(torch.Tensor(1))
        self.spline_coeffs = nn.Parameter(
            torch.Tensor(num_splines, dim)
        )
        self.b_spline = BSplineBasis(spline_order, num_splines)
        
        self.reset_parameters()
        
    def reset_parameters(self):
        init.xavier_normal_(self.spline_coeffs)
        init.constant_(self.w, 1.0)
        
    def forward(self, x: Tensor):
        batch_size, seq_len, _ = x.shape
        x_reshaped = x.view(-1, self.dim)  # Flatten to (batch_size * seq_len, dim)
        
        basis = torch.sigmoid(x_reshaped) * x_reshaped
        spline_values = self.b_spline(x_reshaped)  # Compute B-spline basis values correctly now
        spline = torch.matmul(spline_values, self.spline_coeffs)
        
        activation = self.w * (basis + spline.view(batch_size, seq_len, -1))
        return activation


x = torch.randn(10, 5, 3)
model = KAN(
    dim = 3,
    depth = 5,
    alpha = 1.0,
    num_splines = 10,
    spline_order = 3
)
out = model(x)
print(out)