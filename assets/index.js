window.onload = () => {
    fetch("/list.json", {
        method: "GET"
    }).then(res => res.json())
        .then(res => {
            window.tips = res

            renderList()
        })
}

function renderList() {
    // TODO fade in the categories instead of jumping

    window.tips["categories"].forEach((category) => {
        name = category["name"]
        image_path = "/assets/" + category["image"]
        description = category["description"]
        count = category["count"]
        tips = category["tips"]

        template = `<div class="category">
            <div class="category-top">
                <img src="[IMAGE_PATH]" class="category-img [SHOULDCROP]">
                <p class="category-name">[NAME]</p>
                <p class="category-count">[COUNT]</p>
            </div>

            <div class="random-msgs">
                <div class="message">
                    [RANDOM_MSG_1]
                </div>
                <div class="message">
                    [RANDOM_MSG_2]
                </div>
                <div class="message">
                    [RANDOM_MSG_3]
                </div>
            </div>
        </div>`.replace("[IMAGE_PATH]", image_path)
            .replace("[NAME]", name)
            .replace("[COUNT]", count)

        if (category["circleCrop"]) {
            template = template.replace("[SHOULDCROP]", "circlecrop")
        } else {
            template = template.replace(" [SHOULDCROP]", "")
        }

        if (count > 3) {
            firstInt = getRandomInt(0, count)
            secondInt = firstInt
            while (secondInt == firstInt) {
                secondInt = getRandomInt(0, count)
            }

            thirdInt = secondInt

            while (thirdInt == secondInt || thirdInt == firstInt) {
                thirdInt = getRandomInt(0, count)
            }

            template.replace("[RANDOM_MSG_1]", sanitize(tips[firstInt]["text"]))
            template.replace("[RANDOM_MSG_2]", sanitize(tips[secondInt]["text"]))
            template.replace("[RANDOM_MSG_3]", sanitize(tips[thirdInt]["text"]))

        }

        document.getElementById("categories").innerHTML = document.getElementById("categories").innerHTML + template
    })

    document.getElementById("loading-msg-here").remove()
    window.loaded = true;
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
}

function sanitize(string) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        "/": '&#x2F;',
    };
    const reg = /[&<>"'/]/ig;
    return string.replace(reg, (match) => (map[match]));
}

setTimeout(function () {
    if (window.loaded) {
        return;
    }
    document.getElementById("loading-msg-here").innerHTML = '<p class="loading-msg" id="loading-msg">Loading</p>'
}, 300)