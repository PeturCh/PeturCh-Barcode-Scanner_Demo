import cv2
import re
from pyzbar.pyzbar import decode
import webbrowser

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    reg_exp_http = 'https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)'
    opened_sites = []
    read_barcodes = []
    if cap.isOpened():
        print("webCam opened")
        while cv2.waitKey(30) != ord('q'):
            ret, frame = cap.read()
            barcodes = decode(frame)

            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)

                #optional if we dont want to print the scanned data again
                if barcode.data not in read_barcodes:
                    read_barcodes.append(barcode.data)
                    print(barcode.data)
                    print(barcode.type)

                if barcode.type == 'QRCODE':
                    site_url = re.match(reg_exp_http, bytes(barcode.data).decode('UTF-8'))
                    #the check for the site is necessary in order not to open many windows
                    if site_url is not None and site_url[0] not in opened_sites:
                        webbrowser.open(site_url[0])
                        opened_sites.append(site_url[0])

            cv2.imshow('Barcode scanner', frame)
