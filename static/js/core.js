document.addEventListener("DOMContentLoaded", function() {
 
    document.addEventListener("scroll", function () {
        let scrollpos = window.scrollY;
        let header = document.getElementById("header");
        let navaction = document.getElementById("navAction");
        let toToggle = document.querySelectorAll(".toggleColour");
        const background_color = "bg-gray-100"

        if (header && navaction)
        {

            /*Apply classes for slide in bar*/
            scrollpos = window.scrollY;

            if (scrollpos > 10) {
                header.classList.add(background_color);
                navaction.classList.remove("bg-white");
                navaction.classList.add("gradient");
                navaction.classList.remove("text-gray-800");
                navaction.classList.add("text-white");
                // Use to switch toggleColour colours
                for (let i = 0; i < toToggle.length; i++) {
                    toToggle[i].classList.add("text-gray-800");
                    toToggle[i].classList.remove("text-white");
                }
                header.classList.add("shadow");
            } else {
                header.classList.remove(background_color);
                navaction.classList.remove("gradient");
                navaction.classList.add("bg-white");
                navaction.classList.remove("text-white");
                navaction.classList.add("text-gray-800");
                //Use to switch toggleColour colours
                for (let i = 0; i < toToggle.length; i++) {
                    toToggle[i].classList.add("text-white");
                    toToggle[i].classList.remove("text-gray-800");
                }

                header.classList.remove("shadow");
            }
        }
    });


});