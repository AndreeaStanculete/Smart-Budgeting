
(() => {
  
    const width = 320; 
    let height = 0; 
    let streaming = false;

    let video = null;
    let canvas = null;
    let photo = null;
    let startbutton = null;
  
    function showViewLiveResultButton() {
      if (window.self !== window.top) {
        document.querySelector(".contentarea").remove();
        const button = document.createElement("button");
        button.textContent = "View live result of the example code above";
        document.body.append(button);
        button.addEventListener("click", () => window.open(location.href));
        return true;
      }
      return false;
    }
  
    function startup() {
      startbutton = document.getElementById("startbutton");
      if (showViewLiveResultButton()) {
        startbutton.disabled=false;
        return;
      }

      

      video = document.getElementById("video");
      canvas = document.getElementById("canvas");
      photo = document.getElementById("photo");
      tryagainbutton = document.getElementById("tryagain");
      sendbutton = document.getElementById("sendbutton");
  
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          video.srcObject = stream;
          video.play();
        })
        .catch((err) => {
          console.error(`An error occurred: ${err}`);
        });
  
      video.addEventListener(
        "canplay",
        (ev) => {
          if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);
  
            // Firefox currently has a bug where the height can't be read from
            // the video, so we will make assumptions if this happens.
  
            if (isNaN(height)) {
              height = width / (4 / 3);
            }
  
            video.setAttribute("width", width);
            video.setAttribute("height", height);
            canvas.setAttribute("width", width);
            canvas.setAttribute("height", height);
            streaming = true;
          }
        },
        false,
      );
  
      startbutton.addEventListener(
        "click",
        (ev) => {
          takepicture();
          ev.preventDefault();
        },
        false,
      );

      tryagainbutton.addEventListener(
        "click",
        (ev) => {
          photo.style.display="none";
          tryagainbutton.style.display="none";
          sendbutton.disabled=true;
          video.style.display="block";
          startbutton.style.display="block";
          ev.preventDefault();
        },
        false,
      );

      sendbutton.addEventListener(
        "click",
        (ev) => {
            const fileInput = document.getElementById('photoFile');

            // Create a new File object
            const myFile = new File(['receipt'], photo.getAttribute("src"), {
                type: 'image/png',
                lastModified: new Date(),
            });

            // Now let's create a DataTransfer to get a FileList
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(myFile);
            fileInput.files = dataTransfer.files;
        }, 
        false,
      );
  
      clearphoto();
    }
  
    // Fill the photo with an indication that none has been
    // captured.
  
    function clearphoto() {
      const context = canvas.getContext("2d");
      context.fillStyle = "#AAA";
      context.fillRect(0, 0, canvas.width, canvas.height);
  
      const data = canvas.toDataURL("image/png");
      photo.setAttribute("src", data);
    }
  
    // Capture a photo by fetching the current contents of the video
    // and drawing it into a canvas, then converting that to a PNG
    // format data URL. By drawing it on an offscreen canvas and then
    // drawing that to the screen, we can change its size and/or apply
    // other changes before drawing it.
  
    function takepicture() {
      const context = canvas.getContext("2d");
      if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);
  
        const data = canvas.toDataURL("image/jpeg");
        photo.setAttribute("src", data);

        photo.style.display="block";
        tryagainbutton.style.display="block";
        sendbutton.disabled=false;

        video.style.display="none";
        startbutton.style.display="none";

      } else {
        clearphoto();

        photo.style.display="none";
        tryagainbutton.style.display="none";
        sendbutton.disabled=true;

        video.style.display="block";
        startbutton.style.display="block";
      }
    }
  
    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener("load", startup, false);
  })();