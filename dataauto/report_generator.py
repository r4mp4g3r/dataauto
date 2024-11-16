# dataauto/report_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.utils import ImageReader  # Import ImageReader
import sys

def generate_report(df, output_report='data_report.pdf'):
    """
    Generate a PDF report summarizing the DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        output_report (str): Path to save the PDF report.

    Returns:
        None
    """
    try:
        c = canvas.Canvas(output_report, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 50, "DataAuto Report")

        # Summary Statistics
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 100, "Summary Statistics:")
        summary = df.describe(include='all').to_string()
        text = c.beginText(50, height - 120)
        text.setFont("Helvetica", 10)
        for line in summary.split('\n'):
            text.textLine(line)
        c.drawText(text)

        # Correlation Heatmap
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr()

            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            plt.title("Correlation Heatmap")
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            image = ImageReader(buf)  # Create an ImageReader object
            c.drawImage(image, 50, height - 500, width=500, height=300)  # Use ImageReader
            buf.close()

        c.save()
        print(f"Report generated successfully and saved to {output_report}.")

    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)