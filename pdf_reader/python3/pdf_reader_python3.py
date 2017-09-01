# -*- coding: utf-8 -*-
"""Playbook app to read a PDF (should work for python3.x)."""

from io import StringIO
import os
import tempfile
import traceback

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from tcex import TcEx


def parse_arguments():
    """Parse arguments coming into the app."""
    # retrieve a string as an argument
    tcex.parser.add_argument('--pdf_content', help='Content of the PDF', required=True)
    return tcex.args


def convert_pdf_to_txt(pdf_content):
    """Parse the incoming contents as if it were a PDF and return the text."""
    # create a tempfile that is not deleted when it is closed (hence the `delete=False`)
    temp_pdf = tempfile.NamedTemporaryFile(delete=False)
    # write the pdf content to a tempfile
    temp_pdf.write(pdf_content)
    # close the stream to the tempfile
    temp_pdf.close()

    # initialize a pdfminer TextConverter and the necessary configurations
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    # initialize an interpreter
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # read the pdf content from the tempfile (creating a file pointer pointing to a simulated pdf file)
    fp = open(temp_pdf.name, 'rb')

    # various pdf configurations
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    # parse and read each page of the pdf
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    # get the text!
    text = retstr.getvalue()

    # close up shop... close the open streams and remove the tempfile (`os.unlink...`)
    os.unlink(temp_pdf.name)
    fp.close()
    device.close()
    retstr.close()

    # return the string
    return text


def main():
    """Parse the incoming PDF contents as a PDF."""
    # handle the incoming arguments
    args = parse_arguments()

    # read the pdf_content from the tcex playbook to get the actual value of the pdf content
    pdf_content = tcex.playbook.read(args.pdf_content)

    # get the text from the PDF contents
    text = convert_pdf_to_txt(pdf_content)

    # output the text as a variable for downstream apps
    tcex.playbook.create_output('pdf.reader.text', text)

    # hasta luego
    tcex.exit()


if __name__ == "__main__":
    # initialize a TcEx instance
    tcex = TcEx()
    try:
        # start the app
        main()
    except SystemExit:
        pass
    except:  # if there are any strange errors, log it to the logging in the UI
        err = 'Generic Error. See logs for more details.'
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(err)
        tcex.playbook.exit(1)
