import os

import cv2
import glob
import re
from natsort import natsorted

def Create():
    # 保存の画像Path
    screenshot_path = "01_ScreenShot/*"
    copy_image_path = "02_Copy_ScreenShot/"
    output_image_path = "03_Output/"
    # 拡張子
    image_extension = ".png"

    # 画像複製
    screenshot_files_path = sorted(glob.glob(screenshot_path))
    for screenshot_file_index, screenshot_file in enumerate(screenshot_files_path):
        read_screenshot = cv2.imread(str(screenshot_file))  # 画像読み込み
        copy_screenshot = read_screenshot.copy()  # 画像複製
        cv2.imwrite(copy_image_path + str(screenshot_file_index) + image_extension,
                    copy_screenshot)  # Copy_ScreenShotディレクトリに画像書き出し
    print("01　Copy Finish")

    # 複製した画像を90度回転させる
    copy_screenshot_files_path = sorted(glob.glob(copy_image_path + "*"))
    for copy_screenshot_files_index, copy_screenshot_file in enumerate(copy_screenshot_files_path):
        read_screenshot_image = cv2.imread(
            copy_image_path + str(copy_screenshot_files_index) + image_extension)  # 複製した画像読み込み
        img_rotate_90_counterclockwise = cv2.rotate(read_screenshot_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 90度半時計回転
        cv2.imwrite(copy_image_path + str(copy_screenshot_files_index) + image_extension,
                    img_rotate_90_counterclockwise)  # Copy_ScreenShotディレクトリに90度半時計で回転した画像書き出し
    print("02 ImageRotate Finish")

    # SCAN画像結合する
    max_height = 0
    max_width = 0
    for create_image_index, create_image_file in enumerate(copy_screenshot_files_path):
        if create_image_index == 0:
            img1 = cv2.imread(copy_image_path + str(create_image_index) + image_extension)
            img2 = cv2.imread(copy_image_path + str(create_image_index + 1) + image_extension)
            # SCAN画像合成する
            stitcher_scan = cv2.Stitcher.create(cv2.Stitcher_SCANS)
            status2, stitched_scan = stitcher_scan.stitch([img1, img2])
            # SCAN画像を保存する
            cv2.imwrite(output_image_path + "scan" + image_extension, stitched_scan)
        elif create_image_index >1 :
            # 複製した画像を大きい値にリサイズする（小さい値が正解？ここ大事な気がするので後修正必要）
            # height,widthの最大を取得する。もっと簡単に関数でとれんか？
            for copy_files_index, copy_file in enumerate(copy_screenshot_files_path):
                image = cv2.imread(copy_file)
                if image is not None:
                    height, width, color = image.shape
                    max_height = max(max_height, height)
                    max_width = max(max_width, width)
            print(max_height)
            print(max_width)
            #　全部の画像をmax_height,max_width更新させる。
            for resize_files_index,resize_file in enumerate(copy_screenshot_files_path):
                if (resize_files_index >1) and (resize_files_index<len(copy_screenshot_files_path)):
                    resize_image = cv2.resize(cv2.imread(resize_file), (max_width, max_height))# リサイズ成功
                    cv2.imwrite(copy_image_path + str(resize_files_index) + image_extension,resize_image)

                    img1 = cv2.imread(output_image_path+"scan" + image_extension)
                    img2 = cv2.imread(copy_image_path + str(resize_files_index) + image_extension)
                    # SCAN画像合成する
                    stitcher_scan_ = cv2.Stitcher.create(cv2.Stitcher_SCANS)
                    status2_, stitched_scan_ = stitcher_scan_.stitch([img1, img2])
                    # SCAN画像を保存する
                    cv2.imwrite(output_image_path + "scan" + image_extension, stitched_scan_)
    print("03 CreateImage Finish")

    # 横に回転した画像を縦に戻す
    output_image_file_path = sorted(glob.glob(output_image_path + "*"))
    for img_index, img_file in enumerate(output_image_file_path):
        read_image_output = cv2.imread(img_file)  # 複製した画像読み込み
        output_image_rotate_90_clockwise = cv2.rotate(read_image_output, cv2.ROTATE_90_CLOCKWISE)  # 90度回転
        # 正規表現で ./03_Output/以降の画像ファイル名.拡張子を取得
        s = glob.glob(output_image_path + "*")
        # print(str(s[img_index]))
        p = r'03_Output/(.*)'
        m = re.search(p, str(s[img_index]))
        # 書き出し
        cv2.imwrite(output_image_path + str(m.group(1)), output_image_rotate_90_clockwise)
    print("04 ImageRotate2 Finish")
    print("ALL Finish Successfully")

Create()

