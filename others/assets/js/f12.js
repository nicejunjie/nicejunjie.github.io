"use strict";

console.log("getting user media");

navigator.mediaDevices.getUserMedia({
    video: false, audio: true
}).then(stream => {
    const ac = new AudioContext();
    const source = ac.createMediaStreamSource(stream);
    const analyser = ac.createAnalyser();
    analyser.fftSize = 2048*4;
    //analyser.maxDecibels = 0; //default -30
    //analyser.minDecibels = -70; //default -100
    analyser.smoothingTimeConstant = 0.8; //default 0.8
    console.dir(analyser);

    const lp = ac.createBiquadFilter(); //lowpass to cut noise
    source.connect(lp);
    lp.connect(analyser);

    //analyser.connect(ac.destination); // to speaker
    //console.log(ac.sampleRate);

    /*
       {
    // color list of 12 keys
    const colors = document.createElement("h2");
    document.body.appendChild(colors);
    colors.textContent = "key colors: ";
    const keys = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
    ];
    const lp = ac.createBiquadFilter(); //lowpass to cut noise
    lp.connect(ac.destination);
    keys.forEach((key, index) => {
    const keyfreq = 440 * Math.pow(2, (index - 9) / 12);
    const i = keyfreq / (ac.sampleRate / analyser.fftSize);
    const e = document.createElement("span");
    e.textContent = `${key}`;
    e.style.backgroundColor = `hsl(${indexHue(i)}, 50%, 50%)`;
    e.style.display = "inline-block";
    e.style.textAlign = "center";
    e.style.width = "50px";
    e.addEventListener("click", ev => {
    const osc = ac.createOscillator();
    osc.frequency.value = keyfreq;
    //osc.type = "square";
    osc.start(ac.currentTime);
    osc.stop(ac.currentTime + 1);
    osc.connect(lp);
    }, false);
    colors.appendChild(e);
    });
    }
    */

    // render sample and freqency
    /*
       const canvas = document.createElement("canvas");
       canvas.width = 800;
       canvas.height = 600;
       document.body.appendChild(canvas);
       */
    const canvas = document.getElementById("canvas");
    canvas.width = canvas.clientWidth;
    canvas.height = 800;

    const c2d = canvas.getContext("2d");
    // [constants]
    // ac.sampleRate(44100): sampling rate for FFT
    // analyser.fftSize(2048): data size
    // analyser.frequencyBinCount(1024) = fftSize/2:
    //    As Fourier Trans, use k = from -1024 to 1024, but F(-k) = ~F(k)
    //     (cos parts are same, sin parts as negated)
    //    Usually store only k = from 0 to 1024
    // analyser.smoothingTimeConstant(0.8): s*F_cur + (1-s)*F_prev
    //    (as noise remove)

    // power of "time domain data"(=sampled gain) as 0-255
    // (window function applyed: reducing weight from center to past/future)
    const tds = new Uint8Array(analyser.fftSize); //2048 by default?
    // power of frequencies (0-255 rate) as dB(= 20*log10(|gain_of_freq|))
    // (smoothing filter applyied)
    const freqs = new Uint8Array(analyser.frequencyBinCount);

    function indexHue(index) {
        return (Math.log2(index) % 1) * 360; // coloring by octave
    }

    let keyuse = [];
    //let keyuse_sum = [];
    for(var i = 0;i < 12; ++i) {
      keyuse[i] = 20;
      //keyuse_sum[i] = 0;
    }

    let frames = 0;
    (function draw() {
        requestAnimationFrame(_ => {
            frames++;
            analyser.getByteFrequencyData(freqs);
            analyser.getByteTimeDomainData(tds);
            c2d.clearRect(0, 0, canvas.width, canvas.height);
            //c2d.save();
            //c2d.scale(canvas.width / analyser.fftSize, canvas.height / 600);

            /*
            //find the loudest key and use it as key
            const key = freqs.reduce(
            (r, v, i) => { return r.v < v ? {v, i} : r},
            { v: 0, i: 0}
            );
            c2d.fillStyle = `hsl(${indexHue(key.i)}, 50%, 50%)`;
            */

            //console.log(analyser.frequencyBinCount); //1024 by default?

            //draw wave form
            c2d.fillStyle = "gray";
            for (let i = 0; i < analyser.fftSize; i++) {
                const v = tds[i];
                c2d.fillRect(i, canvas.height - v, 1, v);
            }

            /*
            //quantize to nearest 12 keys (1/10 increment)
            let qs = [];
            for (let i = 0; i < 12*10; ++i) qs[i] = 0;
            for (let i = 0; i < analyser.frequencyBinCount; i++) {
                var ckey = Math.log2(i);
                var oct = Math.floor(ckey);
                var key = ckey%1+0.025; //0.025 to adjust to 440Hz tuning 0-1 range)
                var q = Math.floor((12*10)*key);
                if(oct < 5) continue; //ignore low frequency - not accurate
                qs[q] += freqs[i];
            }
            */


            //draw keys
            const keys = [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B" ];
            let d = 2*Math.PI/12;
            for(var key = 0;key < 12;++key) {
                //c2d.lineWidth = keyuse_sum[key]/1000+20;
                c2d.lineWidth = 150;
                c2d.beginPath();
                c2d.arc(canvas.width/2,canvas.height/2,300,key*d+d/4,(key+1)*d-d/4);
                c2d.strokeStyle = "hsl("+(key*30)+", 50%, "+keyuse[key]+"%)";
                c2d.stroke();

                //dim
                if(keyuse[key] > 10) {
                  keyuse[key]-=0.3;
                  //keyuse_sum[key]-=10;
                }
            }

            c2d.fillStyle = 'white';
            c2d.font="25px Verdana";
            for(var key = 0;key < 12;++key) {
                var x = Math.cos((2*Math.PI)*key/12+3.9)*300;
                var y = Math.sin((2*Math.PI)*key/12+3.9)*300;
                c2d.fillText(keys[key], x+canvas.width/2-10, y+canvas.height/2);
            }

            c2d.beginPath();
            c2d.lineWidth = 2;
            var first = true;
            //for (let i = 100; i < analyser.frequencyBinCount; i++) {
            //console.log(analyser.frequencyBinCount); //1014
            var prev_note = null;
            //var prev_vel = [];
            for (let i = 0; i < analyser.frequencyBinCount; i++) {
                let v = freqs[i];
                //calculate radial pos
                var ckey = Math.log2(i);
                var oct = Math.floor(ckey);
                var key = ckey%1;

                if(oct < 4) continue; //ignore low frequency - not accurate

                v+=0;

                //trigger keyuse
                var note = Math.floor(ckey*12);
                var dist = Math.abs(ckey*12 - note);
                var use = v/(dist+0.1)/150*oct;
                //if(frames % 1000 == 0) console.log(dist);
                //if(dist < 0.20) { // && keyuse[note%12] < v/3) {
                if(keyuse[note%12] < use) keyuse[note%12] = use;
                //}

                //TODO - instead of completely stop showing, maybe I should skip a few values?
                if(oct > 8) continue; //don't need to show too high

                var x = Math.cos((2*Math.PI)*key+0.14)*v;
                var y = Math.sin((2*Math.PI)*key+0.14)*v;
                if(first) c2d.moveTo(canvas.width/2+x, canvas.height/2+y);
                first = false;
                c2d.lineTo(canvas.width/2+x, canvas.height/2+y);
                //use different color for each note
                if(prev_note == null) prev_note = note;
                if(prev_note != note) {
                    c2d.strokeStyle = "hsl("+(note*4)+", 90%, 50%)";
                    //c2d.strokeStyle = "hsl(0, 0%, "+(note)+"%)";
                    //console.log(note);
                    c2d.stroke();
                    prev_note = note;
                    c2d.beginPath();
                    c2d.moveTo(canvas.width/2+x, canvas.height/2+y);
                }

                //adjust key color
                //console.log(note%12);
                //if(oct > 6 && v > 200) keyuse[note%12]=50;
            }
            c2d.stroke(); //stroke the rest
            /*
            for (let i = 0; i < 12*10; i++) {
                let v = qs[i];
                var key = i/(12*10);
                var x = Math.cos((2*Math.PI)*key)*(v/5+50);
                var y = Math.sin((2*Math.PI)*key)*(v/5+50);
                if(first) c2d.moveTo(canvas.width/2+x, canvas.height/2+y);
                first = false;
                c2d.lineTo(canvas.width/2+x, canvas.height/2+y);
            }
            */

            //c2d.restore();
            draw();
        });
    })();
}).catch(err => console.log(err));
