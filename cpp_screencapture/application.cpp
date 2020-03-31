#include "ScreenCapture.h"
#include <iostream>
#include <opencv2/core.hpp>

int main()
{
	while (true) {
		cv::Mat buf = screencapture::ToMemory(800, 600);
		cv::imshow("", buf);
		cv::waitKey(50);
	}
	return 0;
}