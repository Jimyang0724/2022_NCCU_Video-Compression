#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "Problem1.hpp"

using namespace std;

Problem1::Problem1(void) {}

// auto Problem1::copyImg(const cv::Mat &img) {
//     cv::Mat copy = cv::Mat::zeros(img.rows, img.cols, img.type());
//     for(int i=0; i<img.rows; i++) {
//         for (int j=0; j<img.cols; j++) {
//             copy.at<cv::Vec3b>(i, j) = img.at<cv::Vec3b>(i, j);
//         }
//     }

//     return copy;
// }

auto Problem1::convertYCrCb444ToYCrCb422(const cv::Mat &img_ORI) {
    int height = img_ORI.rows, width = img_ORI.cols;
    cv::Mat img_420, img_YCrCb444;
    img_ORI.copyTo(img_YCrCb444);

    vector<cv::Mat1b> planes;
    cv::split(img_YCrCb444, planes);

    for(int i=0; i<height; i++) {
        for(int j=0; j<width; j++) {
            cout<<planes[0].at<uchar>(i,j)<<endl;
        }
    }

    // cout<<img_YCrCb444.at<cv::Vec3b>(10, 10)<<endl;

    cv::imshow("image copy", img_YCrCb444);
    cv::waitKey(0);
    
    return img_420;
}

void Problem1::doProblem1(const cv::Mat &img_ORI) {
    cv::Mat img_YCrCb, img_YCrCb420;
    cv::cvtColor(img_ORI, img_YCrCb, cv::COLOR_BGR2YCrCb);

    img_YCrCb420 = convertYCrCb444ToYCrCb422(img_YCrCb);
    // cv::imshow("START PROJECT WITH OPENCV", img_YCrCb420);
    // cv::waitKey(0);
    // cout<<img_ORI.at<cv::Vec3b>(img_ORI.cols, img_ORI.rows)<<endl;
    // cout<<img_ORI.cols<<" "<<img_ORI.rows<<endl;
    // cout<<img_ORI.at<cv::Vec3b>(176, 144)<<endl;
}