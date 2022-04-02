#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "Problem1.hpp"

using namespace std;

int main(int argc, char const *argv[])
{
    /* Read Image */
    cv::Mat image_ORI;
    image_ORI = cv::imread("../images/foreman_qcif_0_rgb.bmp", cv::IMREAD_COLOR);

    cout << "Problem1_" << endl;
    Problem1 p1;
    p1.doProblem1(image_ORI);

    return 0;
}