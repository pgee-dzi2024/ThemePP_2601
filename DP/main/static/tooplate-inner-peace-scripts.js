/*

Tooplate 2143 Inner Peace
https://www.tooplate.com/view/2143-inner-peace

*/

// Mobile menu toggle


       function toggleMenu() {
            const menuToggle = document.querySelector('.menu-toggle');
            const navLinks = document.querySelector('.nav-links');

```
        menuToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
```

}

        document.addEventListener("DOMContentLoaded", function () {

```
        const sections = document.querySelectorAll("section");
        const navLinks = document.querySelectorAll(".nav-link");
        const header = document.querySelector("header");


// Smooth scroll

    navLinks.forEach(link => {

        link.addEventListener("click", function (e) {

            const targetID = this.getAttribute("href");

            if (targetID.startsWith("#")) {

                e.preventDefault();

                const targetSection = document.querySelector(targetID);

            if (targetSection) {

                targetSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        }

    });

});

// Highlight active menu link

        window.addEventListener("scroll", function () {

            let currentSection = "";

            sections.forEach(section => {

                const sectionTop = section.offsetTop - 200;
                const sectionHeight = section.clientHeight;

                if (window.scrollY >= sectionTop) {
                    currentSection = section.getAttribute("id");
                }

            });

        navLinks.forEach(link => {

            link.classList.remove("active");

            const href = link.getAttribute("href").replace("#", "");

            if (href === currentSection) {
                link.classList.add("active");
            }

        });

// Header animation

        if (window.scrollY > 100) {

            header.style.background = "rgba(255,255,255,0.98)";
            header.style.boxShadow = "0 2px 30px rgba(0,0,0,0.1)";

        } else {

            header.style.background = "rgba(255,255,255,0.95)";
            header.style.boxShadow = "0 2px 20px rgba(0,0,0,0.05)";

        }

    });

// Close mobile menu after click

        document.querySelectorAll(".nav-links a").forEach(link => {

            link.addEventListener("click", function () {

                const menuToggle = document.querySelector(".menu-toggle");
                const navContainer = document.querySelector(".nav-links");

                menuToggle.classList.remove("active");
                navContainer.classList.remove("active");

            });

        });
```

        });
            });
                    }
                });
