#ifndef PROJECT_PROBLEM1_H_
#define PROJECT_PROBLEM1_H_

#include <opencv2/opencv.hpp>

class Problem1 {
    public:
        // Constructor
        Problem1(void);

        // Functions
        void doProblem1(const cv::Mat &img_ORI);

    private:
        auto convertYCrCb444ToYCrCb422(const cv::Mat &img_444);
        // auto copyImg(const cv::Mat &img);
};

#endif // PROJECT_PROBLEM1_H_