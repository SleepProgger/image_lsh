(function() {
    "use strict";
    var root = this;
    Uint8Array = Uint8Array || Array;
    
    /**
     * High-quality scale function for canvas or image element
     * 
     * @param {Number|Object}
     *            scale
     * @param {Canvas|Image}
     *            input
     * @param {Canvas|String}
     *            [output] if Canvas or undefined, export by canvas if export ==
     *            'png', export by Image png if export == 'jpeg', export by
     *            Image jpeg if export == 'png-src', export by base64 png string
     *            if export == 'jpeg-src', export by base64 jpeg string
     * @param {Boolean}
     *            [inputRemovable] if not true, original canvas is kept if true,
     *            original canvas is not kept
     * @return {Canvas|String|Image|Boolean} if error, return false
     */
    function scale(scale, input, mode) {
        var sw = input.width, sh = input.height, dw, dh, sourceBuffer = input.data;

        if (!sw || !sh)
            return false
        if (typeof scale === 'object') {
            if (scale.width) {
                dw = scale.width + 0.5 | 0;
                dh = scale.height + 0.5 | 0;
            } else {
                dw = sw * scale.scaleX + 0.5 | 0;
                dh = sh * scale.scaleY + 0.5 | 0;
            }
        } else {
            dw = scale * sw + 0.5 | 0;
            dh = scale * sh + 0.5 | 0;
        }
        var dw4 = dw << 2, sw4 = sw << 2, sx, sy, sindex = 0, dx, dy, dyindex, dindex = 0, idx, idy, isx, isy, w, wx, nwx, wy, nwy, crossX, crossY, dwh4 = dw4
                * dh, tmpBuffer, r, g, b, a, dsy, dsx, newCanvas, newCtx, imageData, byteBuffer, TIMES = 255.99 / 255, row0, row1, row2, row3, col0, col1, col2, col3, scaleX = dw
                / sw, scaleY = dh / sh, scaleXY = scaleX * scaleY;

        // DOWNSCALE
        if (root.Float32Array) {
            tmpBuffer = new Float32Array(dwh4)
        } else {
            tmpBuffer = []
            for (dindex = 0; dindex < dwh4; ++dindex) {
                tmpBuffer[dindex] = 0
            }
        }
        // CREATE float buffer
        for (sy = 0; sy < sh; sy++) {
            dy = sy * scaleY
            idy = dy | 0
            dyindex = idy * dw4
            crossY = (!!((idy - (dy + scaleY | 0)) * (sh - 1 - sy))) << 1
            if (crossY) {
                wy = idy + 1 - dy
                nwy = dy + scaleY - idy - 1
            }
            for (sx = 0; sx < sw; sx++, sindex += 4) {
                dx = sx * scaleX
                idx = dx | 0
                dindex = dyindex + (idx << 2)
                crossX = !!((idx - (dx + scaleX | 0)) * (sw - 1 - sx))
                if (crossX) {
                    wx = idx + 1 - dx
                    nwx = dx + scaleX - idx - 1
                }
                r = sourceBuffer[sindex]
                g = sourceBuffer[sindex + 1]
                b = sourceBuffer[sindex + 2]
                
                switch (crossX + crossY) {
                case 0:
                    tmpBuffer[dindex] += r * scaleXY
                    tmpBuffer[dindex + 1] += g * scaleXY
                    tmpBuffer[dindex + 2] += b * scaleXY
                    break
                case 1:
                    w = wx * scaleY
                    tmpBuffer[dindex] += r * w
                    tmpBuffer[dindex + 1] += g * w
                    tmpBuffer[dindex + 2] += b * w
                    w = nwx * scaleY
                    tmpBuffer[dindex + 4] += r * w
                    tmpBuffer[dindex + 5] += g * w
                    tmpBuffer[dindex + 6] += b * w
                    break
                case 2:
                    w = scaleX * wy
                    tmpBuffer[dindex] += r * w
                    tmpBuffer[dindex + 1] += g * w
                    tmpBuffer[dindex + 2] += b * w
                    w = scaleX * nwy
                    dindex += dw4
                    tmpBuffer[dindex] += r * w
                    tmpBuffer[dindex + 1] += g * w
                    tmpBuffer[dindex + 2] += b * w
                    break
                default:
                    w = wx * wy
                    tmpBuffer[dindex] += r * w
                    tmpBuffer[dindex + 1] += g * w
                    tmpBuffer[dindex + 2] += b * w
                    w = nwx * wy
                    tmpBuffer[dindex + 4] += r * w
                    tmpBuffer[dindex + 5] += g * w
                    tmpBuffer[dindex + 6] += b * w
                    w = wx * nwy
                    dindex += dw4
                    tmpBuffer[dindex] += r * w
                    tmpBuffer[dindex + 1] += g * w
                    tmpBuffer[dindex + 2] += b * w
                    w = nwx * nwy
                    tmpBuffer[dindex + 4] += r * w
                    tmpBuffer[dindex + 5] += g * w
                    tmpBuffer[dindex + 6] += b * w
                    break
                }
            }
        }

        mode = (mode || "").toLowerCase();
        if (mode == 'raw'){
            return tmpBuffer;
        }
        if (mode == 'gray'){
            var out_size = (dwh4 / 4); // dirty
            var byteBuffer = new Uint8Array(out_size);
            var r_weight = 0.299, g_weight = 0.587, b_weight = 0.114;
            for (var i = 0, j = 0; i < dwh4; i += 4, j++) {
                byteBuffer[j] = (((tmpBuffer[i] + 0.5 | 0) * r_weight)
                + ((tmpBuffer[i + 1] + 0.5 | 0) * g_weight)
                + ((tmpBuffer[i + 2] + 0.5 | 0) * b_weight)) +0.5 | 0;
            }
            return byteBuffer;
        }
        var out_size = (dwh4 / 4) * 3; // dirty
        var byteBuffer = new Uint8Array(out_size);
        for (var i = 0, j = 0; i < dwh4; i += 4, j+=3) {
            byteBuffer[j    ] = (tmpBuffer[i    ] + 0.5 | 0);
            byteBuffer[j + 1] = (tmpBuffer[i + 1] + 0.5 | 0);
            byteBuffer[j + 2] = (tmpBuffer[i + 2] + 0.5 | 0);
        }
        return byteBuffer;
        // delete sourceBuffer
    }

    
     function _add(){
         var sum = a.reduce(function(a, b) { return a + b; }, 0);
     }
    
     function hamming_str(a, b){
         var diff = Math.abs(a.length - b.length);
         var min = Math.min(a.length, b.length);
         for(var i=0; i<min; ++i, diff+=a[i]!=b[i]);
         return diff;
     }
    
     function rgb_to_gray(img_data){
         var new_img = new Uint8Array(img_data.length / 3);
         for (var i = 0, j=0; i < img_data.length; i+=3,j++) {
             new_img[j] = 0.299*img_data[i] + 0.587*img_data[i+1] + 0.114*img_data[i+2]
         }
         return new_img;
     }
    
     function strip_alpha(img_data){
         // TODO: check if we can trust in the alpha channel being there 
         var ndata = new Uint8Array((img_data.length / 4) * 3);
         for (var i = 0, j=0; i < img_data.length; i+=4,j+=3) {
             ndata[j] = img_data[i];
             ndata[j+1] = img_data[i+1];
             ndata[j+2] = img_data[i+2];
         }
         return ndata;
     }
    
     function ahash(img_data, width, height){
         console.log(img_data);
         var img = scale({width:width || 8, height: height || 8}, img_data, "gray");
         var reduce = img.reduce || Array.prototype.reduce;
         var sum_ = reduce.call(img, function(a, b) { return a + b; }, 0);
         var avg = (sum_ / img.length) | 0;
         var ret = ""; // TODO use bit aritmethik and return int TODO:
         for (var i = 0; i < img.length; i++) {
             ret += img[i] < avg ? "1" : "0";
         }
         return ret;
     }
    
     function dhash_h(img_data, width, height){
         var ret = "";
         var img = scale({width:width || 8, height: height || 8}, img_data, "gray");
         var x;
         for (var y = 0; y < height; y++) {
            for (x = 1; x < width; x++) {
                ret += img[y * width + x -1] < img[y * width + x] ? "1" : "0" 
            }
         }
         return ret;
     }
     function dhash_v(img_data, width, height){
         var ret = "";
         var img = scale({width:width || 8, height: height || 8}, img_data, "gray");
         var x;
         for (var y = 1; y < height; y++) {
            for (x = 0; x < width; x++) {
                ret += img[(y -1) * width + x] < img[y * width + x] ? "1" : "0" 
            }
         }
         return ret;
     }
    
    
    
    
    // exports
    root.image_lsh = {
            'down_scale_rgb': scale,
            'ahash': ahash,
            'dhash_h': dhash_h,
            'dhash_v': dhash_v,
    }
}.call(this))