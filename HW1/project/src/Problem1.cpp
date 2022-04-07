#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "Problem1.hpp"

using namespace std;

Problem1::Problem1(void) {}

auto Problem1::convertYCrCb444ToYCrCb422(const cv::Mat &img_ORI) {
    int height = img_ORI.rows, width = img_ORI.cols;
    cv::Mat img_420, img_YCrCb444;
    img_ORI.copyTo(img_YCrCb444);

    vector<cv::Mat1b> channels_YCrCb(3);
    cv::split(img_YCrCb444, channels_YCrCb);

    for(int i=0; i<height-1; i+=2) {
        for(int j=0; j<width-1; j+=2) {
            channels_YCrCb[1].at<uchar>(i+1,j) = channels_YCrCb[1].at<uchar>(i,j);
            channels_YCrCb[1].at<uchar>(i,j+1) = channels_YCrCb[1].at<uchar>(i,j);
            channels_YCrCb[1].at<uchar>(i+1,j+1) = channels_YCrCb[1].at<uchar>(i,j);

            channels_YCrCb[2].at<uchar>(i+1,j) = channels_YCrCb[2].at<uchar>(i,j);
            channels_YCrCb[2].at<uchar>(i,j+1) = channels_YCrCb[2].at<uchar>(i,j);
            channels_YCrCb[2].at<uchar>(i+1,j+1) = channels_YCrCb[2].at<uchar>(i,j);

        }
    }
    cv::imshow("Y", channels_YCrCb[0]);
    cv::waitKey(0);
    cv::imshow("Cr_420", channels_YCrCb[1]);
    cv::waitKey(0);
    cv::imshow("Cb_420", channels_YCrCb[2]);
    cv::waitKey(0);

    cv::merge(channels_YCrCb, img_420);
    return img_420;
}

void Problem1::doProblem1(const cv::Mat &img_ORI) {
    cv::Mat img_YCrCb, img_YCrCb420, img_res;
    cv::cvtColor(img_ORI, img_YCrCb, cv::COLOR_BGR2YCrCb);

    img_YCrCb420 = convertYCrCb444ToYCrCb422(img_YCrCb);

    cv::cvtColor(img_YCrCb420, img_res, cv::COLOR_YCrCb2BGR);

    cv::imshow("img_420", img_res);
    cv::waitKey(0);
}