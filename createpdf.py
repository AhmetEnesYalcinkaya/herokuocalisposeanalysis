from fpdf import FPDF
import matplotlib.pyplot as plt
import streamlit as st



def create_pdf(img_fn, pdf_fn):
    """
    Create pdf written to pdf_fn with the image file img_fn.
    """
    pdf = FPDF()
    pdf.add_page()

    # Save to pdf
    pdf.set_xy(30, 50)
    pdf.image(img_fn, w=140, h=110)
    pdf.output(pdf_fn)


def main():
    x = [1, 2, 3, 4, 5, 6]
    y = [1, 5, 3, 5, 7, 8]

    fig1, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(x, y)
    ax2.scatter(x, y)

    st.pyplot(fig1)

    # Save to png
    img_fn = 'Hip angle.png'
    fig1.savefig(img_fn)

    # Prepare file for download.
    dfn = 'angle.png'
    with open(img_fn, "rb") as f:
        st.download_button(
            label="Descarregar imagem",
            data=f,
            file_name=dfn,
            mime="image/png")

    # pdf download
    checkbox = st.checkbox('Name', value='')
    if checkbox:
        pdf_fn = 'mypdf.pdf'
        create_pdf(img_fn, pdf_fn)

        with open(pdf_fn, 'rb') as h_pdf:
            st.download_button(
                label="Descarregar relatório",
                data=h_pdf,
                file_name="Relatório.pdf",
                mime="application/pdf",
            )


if __name__ == '__main__':
    main()