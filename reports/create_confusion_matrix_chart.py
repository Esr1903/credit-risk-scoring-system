import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Confusion matrix değerleri
log_reg_cm = np.array([
    [35, 25],
    [17, 123]
])

balanced_log_reg_cm = np.array([
    [45, 15],
    [38, 102]
])

# Kayıt yolu
output_path = Path(__file__).resolve().parent / "confusion_matrix_comparison.png"

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

matrices = [
    (log_reg_cm, "Logistic Regression", "Purples"),
    (balanced_log_reg_cm, "Balanced Logistic Regression", "YlGnBu")
]

x_labels = ["Tahmin: Kötü", "Tahmin: İyi"]
y_labels = ["Gerçek: Kötü", "Gerçek: İyi"]

for ax, (cm, title, cmap) in zip(axes, matrices):
    im = ax.imshow(cm, cmap=cmap)

    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(x_labels, fontsize=10)
    ax.set_yticklabels(y_labels, fontsize=10)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j, i, str(cm[i, j]),
                ha="center", va="center",
                fontsize=12, fontweight="bold", color="black"
            )

plt.suptitle(
    "Confusion Matrix Karşılaştırması",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Grafik kaydedildi: {output_path}")