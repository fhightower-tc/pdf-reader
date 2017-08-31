# -*- coding: utf-8 -*-
"""Playbook app to read a PDF.."""

from cStringIO import StringIO
import traceback

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from tcex import TcEx


def parse_arguments():
    """Parse arguments coming into the app."""
    # retrieve a string as an argument
    tcex.parser.add_argument('--string', help='Input string', required=True)
    args = tcex.args

    return args


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def main():
    """."""
    # handle the incoming arguments
    args = parse_arguments()

    # get the text from the pdf
    text = convert_pdf_to_txt(args.pdf_content)

    # output the text as a variable for downstream apps
    tcex.playbook.create_output('pdf.reader.text', text)

    # exit
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
