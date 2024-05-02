import torch
from torch import nn
from torchvision import transforms

__all__ = [
    "Unet",
]


class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


class Unet(nn.Module):
    def __init__(
        self,
        in_channels: int = 3,
        out_channels: int = 1,
        features: list[int] = [64, 128, 256, 512],
        bilinear: bool = False,
    ):
        super().__init__()
        self.downs = nn.ModuleList()
        self.ups = nn.ModuleList()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        for feature in features:
            self.downs.append(DoubleConv(in_channels, feature))
            in_channels = feature

        for feature in reversed(features):
            if bilinear:
                self.ups.append(
                    nn.Upsample(scale_factor=2, mode="bilinear", align_corners=True)
                )
                self.ups.append(DoubleConv(feature * 3, feature))
            else:
                self.ups.append(
                    nn.ConvTranspose2d(feature * 2, feature, kernel_size=2, stride=2)
                )
                self.ups.append(DoubleConv(feature * 2, feature))

        self.bottleneck = DoubleConv(features[-1], features[-1] * 2)
        self.final_conv = nn.Conv2d(features[0], out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor):
        skip_connections = []
        for down in self.downs:
            x = down(x)
            skip_connections.append(x)
            x = self.pool(x)
        x = self.bottleneck(x)
        skip_connections = skip_connections[::-1]

        for idx in range(0, len(self.ups), 2):
            x = self.ups[idx](x)
            skip_connection = skip_connections[idx // 2]
            if x.shape != skip_connection.shape:
                x = transforms.Resize(size=skip_connection.shape[-2:])(x)
            concat_skip = torch.cat([skip_connection, x], dim=1)
            x = self.ups[idx + 1](concat_skip)
        return self.final_conv(x)


if __name__ == "__main__":
    b = Unet(
        in_channels=3,
        out_channels=1,
        bilinear=True,
    )
    x = torch.randn(1, 3, 183, 183)
    y = b(x)
    print(y.shape)
