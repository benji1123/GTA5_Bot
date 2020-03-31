#pragma once
#include <iostream>
#include <windows.h>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

namespace screencapture {
	cv::Mat ToMemory(int w = GetSystemMetrics(SM_CXSCREEN), int h = GetSystemMetrics(SM_CYSCREEN));
};