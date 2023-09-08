import cv2
import glob
import re
from PIL import Image

# 　ScreenShot画像からPANORAMA/SCAN画像を合成する関数
def CreateImage():
    # 画像を読み込む。
    img1 = cv2.imread('01_ScreenShot/left.png')
    img2 = cv2.imread('01_ScreenShot/right.png')
    # ２枚の画像の高さと幅をresizeして同じにする　数字は任意で。本当は大きい方に自動的に合わせたかったけど今回割愛　適当にサイズを指定
    img1_resize = cv2.resize(img1, (800, 700))
    img2_resize = cv2.resize(img2, (800, 700))


    # パノラマ合成する。
    stitcher_create = cv2.Stitcher.create()
    status1,stitched_panorama = stitcher_create.stitch([img1_resize, img2_resize])
    #print(status1)
    # パノラマ画像を保存する。
    cv2.imwrite('panorama_output.png', stitched_panorama)


    # スキャンを合成する
    stitcher_scan = cv2.Stitcher.create(cv2.Stitcher_SCANS)
    status2,stitched_scan = stitcher_scan.stitch([img1_resize, img2_resize])
    #print(status2)
    # パノラマ画像を保存する。
    cv2.imwrite('scan_output.png', stitched_scan)

    #作成したパノラマ画像読み込み
    image = cv2.imread('scan_output.png')
    #作成したパノラマ画像を元画像のwidth,heightと同じにしています。
    image_resize = cv2.resize(image, (1472, 800))
    #出力
    cv2.imwrite('resize_output.jpg', image_resize)

    # Scan画像を保存する
    print("CreateFinish")

# 画像を90度反時計回転させる関数
def OpenImage():
    testImg = cv2.imread('01_ScreenShot/test.png')
    print(type(testImg))
    print(testImg.shape)
    # 90度反時計回転
    img_rotate_90_counterclockwise = cv2.rotate(testImg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite('03_Output/rotateOutput.png', img_rotate_90_counterclockwise)

    # 画像を複製する
    rotateImage = cv2.imread('03_Output/rotateOutput.png')
    image = cv2.rotate(rotateImage, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite('03_Output/OpenImage/output.png', image)
    print("OpenImage Function Finish")

# ディレクトリのファイルを全て取得する関数
def GetFileList():
    files = glob.glob("01_ScreenShot/*")  # ディレクトリパス指定
    for index, copyfile in enumerate(files):
        before_image = cv2.imread(str(copyfile))  # 画像読み込み
        copied_image = before_image.copy()  # 画像複製
        cv2.imwrite("03_Output/CopyFile/" + str(index) + '_.png', copied_image)  # 画像書き出し
    print("finish")


# 完成
def Create():
    # 保存の画像Path
    screenshot_path = "01_ScreenShot/*"
    copy_image_path = "02_Copy_ScreenShot/"
    output_image_path = "03_Output/"
    # 拡張子
    image_extension = ".png"

    # ScreenShotにディレクトリの画像をCopy_ScreenShotに複製する
    screenshot_files_path = glob.glob(screenshot_path)  # ディレクトリパス指定
    for screenshot_file_index, screenshot_file in enumerate(screenshot_files_path):
        read_screenshot = cv2.imread(str(screenshot_file))  # 画像読み込み
        copy_screenshot = read_screenshot.copy()  # 画像複製
        cv2.imwrite(copy_image_path + str(screenshot_file_index) + image_extension, copy_screenshot)  # Copy_ScreenShotディレクトリに画像書き出し
    print("01 ImageCopy Finish")

    # 複製した画像を90度回転させる
    copy_screenshot_files_path = glob.glob(copy_image_path + "*")
    for coppy_screenshot_files_index, copy_screenshot_file in enumerate(copy_screenshot_files_path):
        read_screenshot_image = cv2.imread(copy_image_path + str(coppy_screenshot_files_index) + image_extension)  # 複製した画像読み込み
        img_rotate_90_counterclockwise = cv2.rotate(read_screenshot_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 90度半時計回転
        cv2.imwrite(copy_image_path + str(coppy_screenshot_files_index) + image_extension, img_rotate_90_counterclockwise)  # Copy_ScreenShotディレクトリに90度半時計で回転した画像書き出し
    print("02 ImageRotate Finish")

    # PANORAMA画像をSCAN画像を作成
    for create_image_index, create_image_file in enumerate(copy_screenshot_files_path):
        if create_image_index == 0:
            img1 = cv2.imread(copy_image_path + str(create_image_index) + image_extension)
            img2 = cv2.imread(copy_image_path + str(create_image_index+1) + image_extension)
            # PANORAMA画像を合成する。
            stitcher = cv2.Stitcher_create()
            status, stitched = stitcher.stitch([img1, img2])
            # PANORAMA画像を保存する
            cv2.imwrite(output_image_path+"panorama" + image_extension, stitched)
            # SCAN画像合成する
            stitcher_scan = cv2.Stitcher.create(cv2.Stitcher_SCANS)
            status2, stitched_scan = stitcher_scan.stitch([img1, img2])
            # SCAN画像を保存する
            cv2.imwrite(output_image_path+"scan" + image_extension, stitched_scan)
        #elif create_image_index<len(copy_screenshot_files_path):
            # 今は合成画像が２枚に限定しているが、将来２枚以上の場合、合成した画像＋3枚目以降の画像を1枚数ずつ読み込ませて、合成させていく処理をここに書く予定
            # print(create_image_index,len(copy_screenshot_files_path))
    print("03 CreateImage Finish")

    # 横に回転した画像を縦に戻す
    output_image_file_path = glob.glob(output_image_path+"*")
    for img_index,img_file in enumerate(output_image_file_path):
        read_image_output = cv2.imread(img_file)  # 複製した画像読み込み
        output_image_rotate_90_clockwise = cv2.rotate(read_image_output, cv2.ROTATE_90_CLOCKWISE)  # 90度回転
        # 正規表現で ./03_Output/以降の画像ファイル名.拡張子を取得
        s = glob.glob(output_image_path + "*")
        # print(str(s[img_index]))
        p = r'03_Output/(.*)'
        m = re.search(p, str(s[img_index]))
        # print(str(m.group(1)))
        # 書き出し
        cv2.imwrite(output_image_path+str(m.group(1)), output_image_rotate_90_clockwise)
    print("04 ImageRotate2 Finish")
    print("ALL Finish Successfully")

# CreateImage()
# OpenImage()
# GetFileList()
#Create()


