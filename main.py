import binascii
import re
import argparse
from functools import reduce

formatRegex = {'png': '89504E47(.+?)49454E44AE426082',
               'jpg': 'FFD8FFE0(.+?)FFD9',
               'gif': '47494638(.+?)3B'}

def fileOpen(filename):
    with open(filename, 'rb') as f:
        hex_data = binascii.hexlify(f.read())
        hex_data = str(hex_data).upper().lstrip("B'").rstrip('\'')
        return hex_data

def getExtension(value):
    for key, val in formatRegex.items():
        if val == value:
            return key
    return None

def writeToFile(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def normalizeData(data):
    data = data.strip()
    data = data.replace(' ', '')
    data = data.replace('\n', '')
    return data

def extractImages(hex_data, format):
    incInt = 0
    rr = re.findall(format, hex_data)
    formatExtension = getExtension(format)
    for img in rr:
        if img is not None:
            regStart = format.split("(")[0]
            regEnd = format.split(")")[1]
            data = regStart + img + regEnd

            data = normalizeData(data)
            data = binascii.a2b_hex(data)

            filename = "image" + str(incInt) + "." + formatExtension

            writeToFile(filename, data)
            incInt += 1

def getFileExtensions(filename):
    return filename.split(".")[-1]

def getFileName(filename):
    return filename.split(".")[0]

def getSizeOfData(data):
    return len(data)

def replaceImage(inputFile, replaceImage, inputFileImageIndex, originalExtension, originalName, format):
    incInt = 0
    r1 = re.findall(formatRegex[format], replaceImage)
    rr = re.findall(formatRegex[format], inputFile)
    for img in rr:
        if img is not None:
            if incInt == inputFileImageIndex:
                print("Found image to replace")
                regStart = formatRegex[format].split("(")[0]
                regEnd = formatRegex[format].split(")")[1]
                data = regStart + img + regEnd
                data = normalizeData(data)
                calcDiff = getSizeOfData(replaceImage) - getSizeOfData(data)
                if calcDiff > 0:
                    print("New image is larger than original image")
                    return
                for im in r1:
                    outputData = formatRegex[format].split(
                        "(")[0] + normalizeData(im) + formatRegex[format].split(")")[1] + ("00" * abs(int(calcDiff/2)))
                    print(outputData)
                outputFile = inputFile.replace(data, outputData)
                outputFile = normalizeData(outputFile)
                outputFile = binascii.unhexlify(outputFile)
                newName = originalName + "_replaced." + originalExtension
                writeToFile(newName, outputFile)
                print("Original file replaced with new image")
                print("New file saved as: " + newName)
                return
            incInt += 1

if __name__ == '__main__':
    argpar = argparse.ArgumentParser()
    argpar.add_argument('-f', '--file', help='File to extract images from')
    argpar.add_argument('-t', '--type', help='Type of image to extract')
    argpar.add_argument('-r', '--replace', help='Replace image path')
    argpar.add_argument('-i', '--index', help='Index of image to replace')
    args = argpar.parse_args()
    if args.file is not None and args.type is not None:
        hex_data = fileOpen(args.file)
        if args.type:
            if args.type in formatRegex:
                extractImages(hex_data, formatRegex[args.type])
            else:
                print('Invalid format')

    if args.file is not None and args.replace is not None:
        originalFileData = fileOpen(args.file)
        replaceImageData = fileOpen(args.replace)
        if args.index is not None and args.type is not None:
            originalExtension = getFileExtensions(args.file)
            originalName = getFileName(args.file)
            replaceImage(originalFileData, replaceImageData, int(
                args.index), originalExtension, originalName, args.type)
        else:
            print('No index specified')
