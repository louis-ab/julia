#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void julia(const double cx, const double cy, const double xs, const double xf, const double ys, const double yf, const int xpix, const int prec, int *im){
    double res = (xf-xs)/xpix; //resolution
    int ypix = (yf-ys)/res; //height in pixels
    
    for(int i=0;i<ypix;i++){
        for(int j=0;j<xpix;j++){
            // initial position based on position in image
            double x = xs+j*res;
            double y = yf-i*res;
            int t = 0; //iteration number
            double xn,yn;
            while(t<prec && x*x+y*y<4){ //runs until it diverges or prec iterations
                xn = x*x-y*y+cx;
                yn = 2*x*y+cy;
                x = xn;
                y = yn;
                t++;
            }
            if(t==prec){ //black
                im[3*(i*xpix+j)] = 0;
                im[3*(i*xpix+j)+1] = 0;
                im[3*(i*xpix+j)+2] = 0;
            }
            else{ // color based on divergence time
                int r,g,b;
                t = log10(100*t/prec+1)*500;
                if(t>800){
                    t -= 800;
                    r = 255;
                    g = 55+t;
                    b = 55+t;
                } else if(t>600){
                    t -= 600;
                    r = 255;
                    g = 255-t;
                    b = 55;
                } else if(t>400){
                    t -= 400;
                    r = 55+t;
                    g = 255;
                    b = 55;
                } else if(t>200){
                    t -= 200;
                    r = 55;
                    g = 255;
                    b = 255-t;
                } else{
                    r = 55;
                    g = 55+t;
                    b = 255;
                }
                im[3*(i*xpix+j)] = r;
                im[3*(i*xpix+j)+1] = g;
                im[3*(i*xpix+j)+2] = b;
            }
        }
    }
}
