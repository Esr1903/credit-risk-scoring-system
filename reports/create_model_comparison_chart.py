from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Model sonuçları
model_results = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "Balanced Logistic Regression"
    ],
    "Accuracy": [0.79, 0.715, 0.785, 0.735],
    "Bad Credit Recall": [0.58, 0.57, 0.42, 0.75]
})

# Çıktı klasörü
current_file = Path(__file__).resolve()
reports_dir = current_file.parent
output_path = reports_dir / "model_comparison_chart.png"

# Grafik boyutu
plt.figure(figsize=(10, 6))

# X ekseni konumları
x = np.arange(len(model_results["Model"]))
width = 0.35

# Sütunlar
plt.bar(x - width/2, model_results["Accuracy"], width, label="Accuracy")
plt.bar(x + width/2, model_results["Bad Credit Recall"], width, label="Bad Credit Recall")

# Başlık ve eksenler
plt.title("Model Comparison: Accuracy vs Bad Credit Recall", fontsize=13, fontweight="bold")
plt.ylabel("Score", fontsize=11)
plt.ylim(0, 1.0)
plt.xticks(x, model_results["Model"], rotation=15, ha="right")
plt.legend()

# Değerleri sütunların üstüne yaz
for i, value in enumerate(model_results["Accuracy"]):
    plt.text(i - width/2, value + 0.02, f"{value:.3f}", ha="center", fontsize=9)

for i, value in enumerate(model_results["Bad Credit Recall"]):
    plt.text(i + width/2, value + 0.02, f"{value:.3f}", ha="center", fontsize=9)

plt.tight_layout()

# PNG olarak kaydet
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print("Grafik başarıyla oluşturuldu:")
print(output_path)