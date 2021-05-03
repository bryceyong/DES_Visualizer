from flask import Flask, render_template, redirect, url_for, request
import binascii
import flask

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "POST":

        req = request.form

        text = req["text"]
        key = req["key"]

        binText = str(''.join(format(ord(i), '08b') for i in text))
        binKey = str(''.join(format(ord(i), '08b') for i in key))

        print(binKey)
        print(binText)

        while len(binText) < 64:
            binText = "0" + binText

        while len(binKey) != 64:
            binKey = "0" + binKey

        # binText = "0100100101000101010011110100011001001001010101000010001100110011"

        # binKey = "0100100101000101010011110100011001001001010101000010001100110001"

        print(binText)
        print(binKey)

        # initial permutation
        permuteKey1 = [57, 49, 41, 33, 25, 17, 9,
                       1, 58, 50, 42, 34, 26, 18,
                       10, 2, 59, 51, 43, 35, 27,
                       19, 11, 3, 60, 52, 44, 36,
                       63, 55, 47, 39, 31, 23, 15,
                       7, 62, 54, 46, 38, 30, 22,
                       14, 6, 61, 53, 45, 37, 29,
                       21, 13, 5, 28, 20, 12, 4]

        permuteKey2 = [14, 17, 11, 24, 1, 5,
                       3, 28, 15, 6, 21, 10,
                       23, 19, 12, 4, 26, 8,
                       16, 7, 27, 20, 13, 2,
                       41, 52, 31, 37, 47, 55,
                       30, 40, 51, 45, 33, 48,
                       44, 49, 39, 56, 34, 53,
                       46, 42, 50, 36, 29, 32]

        permuteText1 = [58, 50, 42, 34, 26, 18, 10, 2,
                        60, 52, 44, 36, 28, 20, 12, 4,
                        62, 54, 46, 38, 30, 22, 14, 6,
                        64, 56, 48, 40, 32, 24, 16, 8,
                        57, 49, 41, 33, 25, 17, 9, 1,
                        59, 51, 43, 35, 27, 19, 11, 3,
                        61, 53, 45, 37, 29, 21, 13, 5,
                        63, 55, 47, 39, 31, 23, 15, 7]

        permuteText2 = [32, 1, 2, 3, 4, 5, 4, 5,
                        6, 7, 8, 9, 8, 9, 10, 11,
                        12, 13, 12, 13, 14, 15, 16, 17,
                        16, 17, 18, 19, 20, 21, 20, 21,
                        22, 23, 24, 25, 24, 25, 26, 27,
                        28, 29, 28, 29, 30, 31, 32, 1]

        check = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                  [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                  [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                  [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

                 [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                  [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                  [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                  [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

                 [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                  [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                  [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                  [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

                 [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                  [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                  [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                  [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

                 [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                  [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                  [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                  [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

                 [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                  [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                  [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                  [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

                 [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                  [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                  [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                  [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

                 [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                  [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                  [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                  [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

        permuteCheck = [16, 7, 20, 21,
                        29, 12, 28, 17,
                        1, 15, 23, 26,
                        5, 18, 31, 10,
                        2, 8, 24, 14,
                        32, 27, 3, 9,
                        19, 13, 30, 6,
                        22, 11, 4, 25]

        permuteFinal = [40, 8, 48, 16, 56, 24, 64, 32,
                        39, 7, 47, 15, 55, 23, 63, 31,
                        38, 6, 46, 14, 54, 22, 62, 30,
                        37, 5, 45, 13, 53, 21, 61, 29,
                        36, 4, 44, 12, 52, 20, 60, 28,
                        35, 3, 43, 11, 51, 19, 59, 27,
                        34, 2, 42, 10, 50, 18, 58, 26,
                        33, 1, 41, 9, 49, 17, 57, 25]

        # initial permutation
        permBinKey = ""
        for i in range(0, 56):
            permBinKey = permBinKey + binKey[permuteKey1[i] - 1]

        # subkey 1
        leftBinKey = permBinKey[0:28]
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        rightBinKey = permBinKey[28:56]
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey1 = ""

        for i in range(0, 48):
            subKey1 = subKey1 + binKey2[permuteKey2[i] - 1]
        print("subKey1 = " + subKey1)
        hexSubKey1 = hex(int(subKey1, 2))
        # subkey 2
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey2 = ""

        for i in range(0, 48):
            subKey2 = subKey2 + binKey2[permuteKey2[i] - 1]
        print("subKey2 = " + subKey2)
        hexSubKey2 = hex(int(subKey2, 2))

        # subkey 3
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey3 = ""

        for i in range(0, 48):
            subKey3 = subKey3 + binKey2[permuteKey2[i] - 1]
        print("subKey3 = " + subKey3)
        hexSubKey3 = hex(int(subKey3, 2))

        # subkey 4
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey4 = ""

        for i in range(0, 48):
            subKey4 = subKey4 + binKey2[permuteKey2[i] - 1]
        print("subKey4 = " + subKey4)
        hexSubKey4 = hex(int(subKey4, 2))

        # subkey 5
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey5 = ""

        for i in range(0, 48):
            subKey5 = subKey5 + binKey2[permuteKey2[i] - 1]
        print("subKey5 = " + subKey5)
        hexSubKey5 = hex(int(subKey5, 2))

        # subkey 6
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey6 = ""

        for i in range(0, 48):
            subKey6 = subKey6 + binKey2[permuteKey2[i] - 1]
        print("subKey6 = " + subKey6)
        hexSubKey6 = hex(int(subKey6, 2))

        # subkey 7
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey7 = ""

        for i in range(0, 48):
            subKey7 = subKey7 + binKey2[permuteKey2[i] - 1]
        print("subKey7 = " + subKey7)
        hexSubKey7 = hex(int(subKey7, 2))

        # subkey 8
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey8 = ""

        for i in range(0, 48):
            subKey8 = subKey8 + binKey2[permuteKey2[i] - 1]
        print("subKey8 = " + subKey8)
        hexSubKey8 = hex(int(subKey8, 2))

        # subkey 9
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey9 = ""

        for i in range(0, 48):
            subKey9 = subKey9 + binKey2[permuteKey2[i] - 1]
        print("subKey9 = " + subKey9)
        hexSubKey9 = hex(int(subKey9, 2))

        # subkey 10
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey10 = ""

        for i in range(0, 48):
            subKey10 = subKey10 + binKey2[permuteKey2[i] - 1]
        print("subKey10 = " + subKey10)
        hexSubKey10 = hex(int(subKey10, 2))

        # subkey 11
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey11 = ""

        for i in range(0, 48):
            subKey11 = subKey11 + binKey2[permuteKey2[i] - 1]
        print("subKey11 = " + subKey11)
        hexSubKey11 = hex(int(subKey11, 2))

        # subkey 12
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey12 = ""

        for i in range(0, 48):
            subKey12 = subKey12 + binKey2[permuteKey2[i] - 1]
        print("subKey12 = " + subKey12)
        hexSubKey12 = hex(int(subKey12, 2))

        # subkey 13
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey13 = ""

        for i in range(0, 48):
            subKey13 = subKey13 + binKey2[permuteKey2[i] - 1]
        print("subKey13 = " + subKey13)
        hexSubKey13 = hex(int(subKey13, 2))

        # subkey 14
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey14 = ""

        for i in range(0, 48):
            subKey14 = subKey14 + binKey2[permuteKey2[i] - 1]
        print("subKey14 = " + subKey14)
        hexSubKey14 = hex(int(subKey14, 2))

        # subkey 15
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp
        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey15 = ""

        for i in range(0, 48):
            subKey15 = subKey15 + binKey2[permuteKey2[i] - 1]
        print("subKey15 = " + subKey15)
        hexSubKey15 = hex(int(subKey15, 2))

        # subkey 16
        temp = leftBinKey[0]
        leftBinKey = leftBinKey[1:]
        leftBinKey = leftBinKey + temp

        temp = rightBinKey[0]
        rightBinKey = rightBinKey[1:]
        rightBinKey = rightBinKey + temp

        binKey2 = leftBinKey + rightBinKey
        subKey16 = ""

        for i in range(0, 48):
            subKey16 = subKey16 + binKey2[permuteKey2[i] - 1]
        print("subKey16 = " + subKey16)
        hexSubKey16 = hex(int(subKey16, 2))

        # message IP
        permBinText = ""
        for i in range(0, 64):
            permBinText = permBinText + binText[permuteText1[i] - 1]
            ip = hex(int(permBinText, 2))
        leftBinText = permBinText[0:32]
        rightBinText = permBinText[32:64]

        # Round 1
        print("Round 1")
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey1[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight1 = XOR2
        newLeft1 = rightBinText

        print(newLeft1)
        print(newRight1)
        round1 = hex(int((newLeft1+newRight1), 2))

        # Round 2
        print("Round 2")
        rightBinText = newRight1
        leftBinText = newLeft1
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey2[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight2 = XOR2
        newLeft2 = rightBinText

        print(newLeft2)
        print(newRight2)
        round2 = hex(int((newLeft2 + newRight2), 2))

        # Round 3
        print("Round 3")
        rightBinText = newRight2
        leftBinText = newLeft2
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey3[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight3 = XOR2
        newLeft3 = rightBinText

        print(newLeft3)
        print(newRight3)
        round3 = hex(int((newLeft3 + newRight3), 2))

        # Round 4
        print("Round 4")
        rightBinText = newRight3
        leftBinText = newLeft3
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey4[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight4 = XOR2
        newLeft4 = rightBinText

        print(newLeft4)
        print(newRight4)
        round4 = hex(int((newLeft4 + newRight4), 2))

        # Round 5
        print("Round 5")
        rightBinText = newRight4
        leftBinText = newLeft4
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey5[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight5 = XOR2
        newLeft5 = rightBinText

        print(newLeft5)
        print(newRight5)
        round5 = hex(int((newLeft5 + newRight5), 2))

        # Round 6
        print("Round 6")
        rightBinText = newRight5
        leftBinText = newLeft5
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey6[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight6 = XOR2
        newLeft6 = rightBinText

        print(newLeft6)
        print(newRight6)
        round6 = hex(int((newLeft6 + newRight6), 2))

        # Round 7
        print("Round 7")
        rightBinText = newRight6
        leftBinText = newLeft6
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey7[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight7 = XOR2
        newLeft7 = rightBinText

        print(newLeft7)
        print(newRight7)
        round7 = hex(int((newLeft7 + newRight7), 2))

        # Round 8
        print("Round 8")
        rightBinText = newRight7
        leftBinText = newLeft7
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey8[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight8 = XOR2
        newLeft8 = rightBinText

        print(newLeft8)
        print(newRight8)
        round8 = hex(int((newLeft8 + newRight8), 2))

        # Round 9
        print("Round 9")
        rightBinText = newRight8
        leftBinText = newLeft8
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey9[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight9 = XOR2
        newLeft9 = rightBinText

        print(newLeft9)
        print(newRight9)
        round9 = hex(int((newLeft9 + newRight9), 2))

        # Round 10
        print("Round 10")
        rightBinText = newRight9
        leftBinText = newLeft9
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey10[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight10 = XOR2
        newLeft10 = rightBinText

        print(newLeft10)
        print(newRight10)
        round10 = hex(int((newLeft10 + newRight10), 2))

        # Round 11
        print("Round 11")
        rightBinText = newRight10
        leftBinText = newLeft10
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey11[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight11 = XOR2
        newLeft11 = rightBinText

        print(newLeft11)
        print(newRight11)
        round11 = hex(int((newLeft11 + newRight11), 2))

        # Round 12
        print("Round 12")
        rightBinText = newRight11
        leftBinText = newLeft11
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey12[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight12 = XOR2
        newLeft12 = rightBinText

        print(newLeft12)
        print(newRight12)
        round12 = hex(int((newLeft12 + newRight12), 2))

        # Round 13
        print("Round 13")
        rightBinText = newRight12
        leftBinText = newLeft12
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey13[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight13 = XOR2
        newLeft13 = rightBinText

        print(newLeft13)
        print(newRight13)
        round13 = hex(int((newLeft13 + newRight13), 2))

        # Round 14
        print("Round 14")
        rightBinText = newRight13
        leftBinText = newLeft13
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey14[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight14 = XOR2
        newLeft14 = rightBinText

        print(newLeft14)
        print(newRight14)
        round14 = hex(int((newLeft14 + newRight14), 2))

        # Round 15
        print("Round 15")
        rightBinText = newRight14
        leftBinText = newLeft14
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey15[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight15 = XOR2
        newLeft15 = rightBinText

        print(newLeft15)
        print(newRight15)
        round15 = hex(int((newLeft15 + newRight15), 2))

        # Round 16
        print("Round 16")
        rightBinText = newRight15
        leftBinText = newLeft15
        padRightBinText = ""
        for i in range(0, 48):
            padRightBinText = padRightBinText + rightBinText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinText[i] == subKey16[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRight16 = XOR2
        newLeft16 = rightBinText

        print(newLeft16)
        print(newRight16)
        round16 = hex(int((newLeft16 + newRight16), 2))

        final = newRight16 + newLeft16

        permFinal = ""
        print("final = " + final)
        for i in range(0, 64):
            permFinal = permFinal + final[permuteFinal[i] - 1]
        print("permFinal = " + permFinal)
        decimal_representation = int(permFinal, 2)
        hexFinal = hex(decimal_representation)
        print("hexFinal = " + hexFinal)

        print()
        print("Decryption:")
        print()
        # Carry out the same steps as above, but apply the subkeys in reverse order

        # Cipher text in binary representation
        binCipherText = bin(int(hexFinal, 16))[2:]

        # Initial Permutation of the Cipher text
        permBinCipherText = ""
        for i in range(0, 64):
            permBinCipherText = permBinCipherText + binCipherText[permuteText1[i] - 1]

        leftBinCipherText = permBinCipherText[0:32]
        rightBinCipherText = permBinCipherText[32:64]

        # Round 1
        print("Round 1")
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey16[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher1 = XOR2
        newLeftCipher1 = rightBinCipherText

        print(newLeftCipher1)
        print(newRightCipher1)

        # Round 2
        print("Round 2")
        rightBinCipherText = newRightCipher1
        leftBinCipherText = newLeftCipher1
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey15[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher2 = XOR2
        newLeftCipher2 = rightBinCipherText

        print(newLeftCipher2)
        print(newRightCipher2)

        # Round 3
        print("Round 3")
        rightBinCipherText = newRightCipher2
        leftBinCipherText = newLeftCipher2
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey14[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher3 = XOR2
        newLeftCipher3 = rightBinCipherText

        print(newLeftCipher3)
        print(newRightCipher3)

        # Round 4
        print("Round 4")
        rightBinCipherText = newRightCipher3
        leftBinCipherText = newLeftCipher3
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey13[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher4 = XOR2
        newLeftCipher4 = rightBinCipherText

        print(newLeftCipher4)
        print(newRightCipher4)

        # Round 5
        print("Round 5")
        rightBinCipherText = newRightCipher4
        leftBinCipherText = newLeftCipher4
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey12[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher5 = XOR2
        newLeftCipher5 = rightBinCipherText

        print(newLeftCipher5)
        print(newRightCipher5)

        # Round 6
        print("Round 6")
        rightBinCipherText = newRightCipher5
        leftBinCipherText = newLeftCipher5
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey11[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher6 = XOR2
        newLeftCipher6 = rightBinCipherText

        print(newLeftCipher6)
        print(newRightCipher6)

        # Round 7
        print("Round 7")
        rightBinCipherText = newRightCipher6
        leftBinCipherText = newLeftCipher6
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey10[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher7 = XOR2
        newLeftCipher7 = rightBinCipherText

        print(newLeftCipher7)
        print(newRightCipher7)

        # Round 8
        print("Round 8")
        rightBinCipherText = newRightCipher7
        leftBinCipherText = newLeftCipher7
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey9[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher8 = XOR2
        newLeftCipher8 = rightBinCipherText

        print(newLeftCipher8)
        print(newRightCipher8)

        # Round 9
        print("Round 9")
        rightBinCipherText = newRightCipher8
        leftBinCipherText = newLeftCipher8
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey8[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher9 = XOR2
        newLeftCipher9 = rightBinCipherText

        print(newLeftCipher9)
        print(newRightCipher9)

        # Round 10
        print("Round 10")
        rightBinCipherText = newRightCipher9
        leftBinCipherText = newLeftCipher9
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey7[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher10 = XOR2
        newLeftCipher10 = rightBinCipherText

        print(newLeftCipher10)
        print(newRightCipher10)

        # Round 11
        print("Round 11")
        rightBinCipherText = newRightCipher10
        leftBinCipherText = newLeftCipher10
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey6[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher11 = XOR2
        newLeftCipher11 = rightBinCipherText

        print(newLeftCipher11)
        print(newRightCipher11)

        # Round 12
        print("Round 12")
        rightBinCipherText = newRightCipher11
        leftBinCipherText = newLeftCipher11
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey5[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher12 = XOR2
        newLeftCipher12 = rightBinCipherText

        print(newLeftCipher12)
        print(newRightCipher12)

        # Round 13
        print("Round 13")
        rightBinCipherText = newRightCipher12
        leftBinCipherText = newLeftCipher12
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey4[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher13 = XOR2
        newLeftCipher13 = rightBinCipherText

        print(newLeftCipher13)
        print(newRightCipher13)

        # Round 14
        print("Round 14")
        rightBinCipherText = newRightCipher13
        leftBinCipherText = newLeftCipher13
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey3[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher14 = XOR2
        newLeftCipher14 = rightBinCipherText

        print(newLeftCipher14)
        print(newRightCipher14)

        # Round 15
        print("Round 15")
        rightBinCipherText = newRightCipher14
        leftBinCipherText = newLeftCipher14
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey2[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher15 = XOR2
        newLeftCipher15 = rightBinCipherText

        print(newLeftCipher15)
        print(newRightCipher15)

        # Round 16
        print("Round 16")
        rightBinCipherText = newRightCipher15
        leftBinCipherText = newLeftCipher15
        padRightBinCipherText = ""
        for i in range(0, 48):
            padRightBinCipherText = padRightBinCipherText + rightBinCipherText[permuteText2[i] - 1]

        XOR1 = ""
        for i in range(0, 48):
            if padRightBinCipherText[i] == subKey1[i]:
                XOR1 = XOR1 + "0"
            else:
                XOR1 = XOR1 + "1"

        # check1
        row1 = XOR1[0] + XOR1[5]
        col1 = XOR1[1:5]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check1 = check[0][row1][col1]
        check1 = "{0:b}".format(int(check1))
        while len(check1) != 4:
            check1 = "0" + check1

        # check2
        row1 = XOR1[6] + XOR1[11]
        col1 = XOR1[7:11]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check2 = check[1][row1][col1]
        check2 = "{0:b}".format(int(check2))
        while len(check2) != 4:
            check2 = "0" + check2

        # check3
        row1 = XOR1[12] + XOR1[17]
        col1 = XOR1[13:17]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check3 = check[2][row1][col1]
        check3 = "{0:b}".format(int(check3))
        while len(check3) != 4:
            check3 = "0" + check3

        # check4
        row1 = XOR1[18] + XOR1[23]
        col1 = XOR1[19:23]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check4 = check[3][row1][col1]
        check4 = "{0:b}".format(int(check4))
        while len(check4) != 4:
            check4 = "0" + check4

        # check5
        row1 = XOR1[24] + XOR1[29]
        col1 = XOR1[25:29]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check5 = check[4][row1][col1]
        check5 = "{0:b}".format(int(check5))
        while len(check5) != 4:
            check5 = "0" + check5

        # check6
        row1 = XOR1[30] + XOR1[35]
        col1 = XOR1[31:35]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check6 = check[5][row1][col1]
        check6 = "{0:b}".format(int(check6))
        while len(check6) != 4:
            check6 = "0" + check6

        # check7
        row1 = XOR1[36] + XOR1[41]
        col1 = XOR1[37:41]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check7 = check[6][row1][col1]
        check7 = "{0:b}".format(int(check7))
        while len(check7) != 4:
            check7 = "0" + check7

        # check8
        row1 = XOR1[42] + XOR1[47]
        col1 = XOR1[43:47]

        row1 = int(row1, 2)
        col1 = int(col1, 2)

        check8 = check[7][row1][col1]
        check8 = "{0:b}".format(int(check8))
        while len(check8) != 4:
            check8 = "0" + check8

        tableData = check1 + check2 + check3 + check4 + check5 + check6 + check7 + check8

        permTableData = ""
        for i in range(0, 32):
            permTableData = permTableData + tableData[permuteCheck[i] - 1]

        XOR2 = ""
        for i in range(0, 32):
            if permTableData[i] == leftBinCipherText[i]:
                XOR2 = XOR2 + "0"
            else:
                XOR2 = XOR2 + "1"

        newRightCipher16 = XOR2
        newLeftCipher16 = rightBinCipherText

        print(newLeftCipher16)
        print(newRightCipher16)

        cipherFinal = newRightCipher16 + newLeftCipher16

        # Carry out the final permutation and print resulting plaintext
        permCipherFinal = ""
        print("cipherFinal = " + cipherFinal)
        for i in range(0, 64):
            permCipherFinal = permCipherFinal + cipherFinal[permuteFinal[i] - 1]
        print("permCipherFinal = " + permCipherFinal)

        decimal_representation_cipher = int(permCipherFinal, 2)
        hexCipherFinal = hex(decimal_representation_cipher)
        print("hexCipherFinal = " + hexCipherFinal)

        byte_array = bytearray.fromhex(hexCipherFinal[2:])
        plaintext = byte_array.decode()
        print("plaintext = " + plaintext)

        return render_template("solution.html", hexSubKey1=hexSubKey1, hexSubKey2=hexSubKey2,
                               hexSubKey3=hexSubKey3, hexSubKey4=hexSubKey4, hexSubKey5=hexSubKey5,
                               hexSubKey6=hexSubKey6, hexSubKey7=hexSubKey7, hexSubKey8=hexSubKey8,
                               hexSubKey9=hexSubKey9, hexSubKey10=hexSubKey10, hexSubKey11=hexSubKey11,
                               hexSubKey12=hexSubKey12, hexSubKey13=hexSubKey13, hexSubKey14=hexSubKey14,
                               hexSubKey15=hexSubKey15, hexSubKey16=hexSubKey16, round1=round1, round2=round2,
                               round3=round3,  round4=round4, round5=round5, round6=round6,
                               round7=round7, round8=round8, round9=round9, round10=round10, round11=round11,
                               round12=round12, round13=round13, round14=round14, round15=round15, round16=round16,
                               hexFinal=hexFinal, permBinText=ip, text=text, key=key)

    return render_template("index.html")

if __name__ == '__main__':
    app.run()