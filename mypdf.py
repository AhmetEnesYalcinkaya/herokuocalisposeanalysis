from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
import consts

def generate_pdf():
    print("I m here")
    pdf_canvas = canvas.Canvas("new.pdf", pagesize=letter)

    # Get the dimensions of the image
    image_width = 150
    image_height = 100
    print(letter[0],letter[1])

    #Text
    text1 = "OCALIS - Ergonomic analysis report n°12879"
    text2= "Do you want to go further to understand the results of the analysis or find a solution adapted to your needs ? "
    text3 = "Contact us : http://www.ocalis.com.tr Phone : +905552988721"

    # Calculate the coordinates to position the image at the top of the page
    x = (letter[0] - image_width) / 2  # Center the image horizontally
    y = letter[1] - image_height - 50  # Place the image 50 units from the top

    # Draw the image onto the canvas
    pdf_canvas.drawImage("image/ocalis.png", x, y, width=image_width, height=image_height)

    #Write Text
    pdf_canvas.setFont("Helvetica", 15)
    pdf_canvas.drawString((letter[0]/2)-150, y-10, text1)
    pdf_canvas.setFont("Helvetica", 10)
    pdf_canvas.drawString((letter[0] - 550), y-50, text2)
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString((letter[0] - 550), y-70, text3)


    #data = [consts.sizes[0], consts.sizes[1]]  # Example data for the pie chart
    data = [60, 40]  # Example data for the pie chart
    labels = ["Label 1", "Label 2"]  # Example labels for each segment

    #Draw graph
    drawing = Drawing(200, 100)

    # Create a Pie chart object
    pie_chart = Pie()
    pie_chart.x = 250
    pie_chart.y = 250
    pie_chart.width = 120
    pie_chart.height = 120
    pie_chart.data = data
    pie_chart.labels = labels

    pie_chart.slices.strokeWidth = 0.5

    # Add the pie chart to the drawing
    drawing.add(pie_chart)

    # Draw the drawing on the canvas
    drawing.drawOn(pdf_canvas, 100, 100)


    # Save and close the PDF canvas
    return pdf_canvas.save()

