(async function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    canvas.width = 640;
    canvas.height = 480;

    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
})();
