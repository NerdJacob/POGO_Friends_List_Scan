# POGO_Friends_List_Scan
Script to scan Pokémon GO friends list screenshots to snapshot progress and assist in identifying inactive friends.

How to:
friends_list.py offers two options for optical character recognition for reading screenshots of your Pokémon GO friends’ list entries placed in the “Inputs” folder and provides a tab separated export of names, wins, distance walked, and number of Pokémon caught for use in comparing values over time and identifying inactive friends.

For Android users, screenshots taken via the “Game Dahsboard” button will not capture the <i>oh so helpful</i> last taken screenshot that covers the bottom left quarter of the screen.

Caveats:
The two options for OCR included are <b>pytesseract</b> and <b>easyocr</b>.  The first is faster, but at this time seems to struggle with these screenshots.  It also requires reference to the local install location for tesseract which <i>may</i> require updating for your copy of the script.  Meanwhile <b>easyocr</b> is much slower but seems to handle these images well.

