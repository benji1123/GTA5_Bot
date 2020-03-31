#include "screencapture.h"

namespace screencapture {

	cv::Mat ToMemory(int captureWidth = GetSystemMetrics(SM_CXSCREEN), int captureHeight = GetSystemMetrics(SM_CYSCREEN)) {

		HDC hwindowDC, hwindowCompatibleDC;
		HBITMAP hbwindow;
		cv::Mat src;
		BITMAPINFOHEADER  bi;

		hwindowDC = GetDC(NULL); // retrieves DC for entire screen
		hwindowCompatibleDC = CreateCompatibleDC(hwindowDC);
		SetStretchBltMode(hwindowCompatibleDC, COLORONCOLOR);

		// create cv::mat container for screen-capture
		src.create(captureHeight, captureWidth, CV_8UC4);

		// create a captureHeight
		hbwindow = CreateCompatibleBitmap(hwindowDC, captureWidth, captureHeight);
		bi.biSize = sizeof(BITMAPINFOHEADER);    //http://msdn.microsoft.com/en-us/library/windows/window/dd183402%28v=vs.85%29.aspx
		bi.biWidth = captureWidth;
		bi.biHeight = -captureHeight;  //this is the line that makes it draw upside down or not
		bi.biPlanes = 1;
		bi.biBitCount = 32;
		bi.biCompression = BI_RGB;
		bi.biSizeImage = 0;
		bi.biXPelsPerMeter = 0;
		bi.biYPelsPerMeter = 0;
		bi.biClrUsed = 0;
		bi.biClrImportant = 0;

		// use the previously created device context with the bitmap
		SelectObject(hwindowCompatibleDC, hbwindow);
		// copy from the window device context to the bitmap device context
		StretchBlt(hwindowCompatibleDC, 0, 0, captureWidth, captureHeight, hwindowDC, 0, 0, captureWidth, captureHeight, SRCCOPY); //change SRCCOPY to NOTSRCCOPY for wacky colors !
		GetDIBits(hwindowCompatibleDC, hbwindow, 0, captureHeight, src.data, (BITMAPINFO*)&bi, DIB_RGB_COLORS);  //copy from hwindowCompatibleDC to hbwindow
		// avoid memory leak
		DeleteObject(hbwindow); DeleteDC(hwindowCompatibleDC); ReleaseDC(NULL, hwindowDC);

		return src;
	}
}