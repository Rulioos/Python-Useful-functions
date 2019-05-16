#include <iostream>
#include <sstream>
#include "string"
#include <vector>
#include <opencv2/opencv.hpp>
#include "Lighten_darken.cpp"

using namespace std;
using namespace cv;

Mat img=imread("mark.jpg");
Mat e=img;

String window1 = "Image";


/*
void reset_all(){
    destroyWindow("Image");
    namedWindow("Image");
}

int new_trackbar(vector<string> line,string name){
    if(img.empty()){

        if(line.size()==1){
            cout<<"You need  at least load an image first"<<endl;
        }else{
            if(loadImage(line[1])!=1){
            }else{
                return 1;
            }
        }
    }

    createTrackbar(name, window1,0, 100);
    return 0;
}
 */
int loadImage(string path) {
    img = imread(path);
    // Check for failure
    if (!img.data) {
        printf(" No image data \n");
        return 1;
    }
    e=img;
    cout << path << " successfully loaded\n";

    return 0;
}


vector<string> splitByChar(string &str, char delim) {
    string buf;                 // Have a buffer string
    stringstream ss(str);       // Insert the string into a stream

    vector<string> tokens; // Create vector to hold our words

    while (getline(ss, buf, delim)) {
        tokens.push_back(buf);
    }
    return tokens;


}

int resize(vector<string> opt) {
    int Xf, x, y;
    vector<string> o;
    if(opt.size()==1 || opt.size()==2) {
        for (auto &i : opt) {
            o = splitByChar(i, '=');
            if (o.size() != 2) {
                cout << "Syntax error on " << i << endl;
                cout << "Syntax is options=value\n";
                return 1;
            } else {
                if (o[0] == "-x") {
                    x = stod(o[1]);
                } else if (o[0] == "-y") {
                    y = stod(o[1]);
                } else if (o[0] == "-X") {
                    std::cout << typeid(o[1]).name() << '\n';
                    Xf = stod(o[1]);

                }
            }
        }
        if (opt.size()==1) {
            //resize by factor;
            resize(img, e, Size(int(img.cols * Xf), int(img.cols * Xf)));
            return 0;
        } else if (opt.size()==2) {
            //resize by coordinates
            resize(img, e, Size(int(x), int(y)));
            return 0;
        } else {
            cout << "Please look to the syntax for resizing\n";
            return 1;
        }
    }else{
        cout<<"Missing options\n";
        return 1;
    }
}

int darken(vector<string> opt) {
    int valContrast;
    int valBrightness;
    lightImg(e,valContrast,valBrightness)
    return 0;
    }

int erosion(vector<string> opt) {
    return 0;
}

int stiching(vector<string> opt) {
    return 0;
}


int main() {
    ofstream log;
    log.open("log.txt");
    vector<string> line;
    string input;
    string command;
    cout << "Enter command line\n";
    while (true) {
        //prints
        imshow(window1,e);
        //
        waitKey();
        cout << ">>";
        //get line
        getline(cin, input);
        //split line
        if (!input.empty()) {
            line = splitByChar(input, ' ');
            //get the command
            command = line[0];

            log << command << endl;
            log.flush();

            //case according the the command entered
            if (command == "resize") {
                //resize the loaded image
                line.erase(line.begin());
                resize(line);

            } else if (command == "load") {
                //load image
                if (line.size() == 2) {
                    loadImage(line[1]);
                }
            } else if (command == "darken" or command == "lighten") {
                //darken/ligthen
                darken(line);
            } else if (command == "dilatation" or command == "erosion") {
                //erosion/dilatation
                erosion(line);
            } else if (command == "help") {
                //print help commands
            }else if (command == "print") {
                //print image by his name. Print edit by default
            } else if (command == "exit") {
                break;
            } else {
                //unknown command message
                cout << "'" << input << "'" << "is an unknown command.help for information.\n";
            }
        }
    }
    destroyAllWindows();


    return 0;
}