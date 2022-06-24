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

    window.tips["categories"].sort((a, b) => {
        return a["count"] - b["count"]
    }).reverse()

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
                <div class="last-updated">
                    [LAST_SUGGESTED_TIME]
</div>
                <div class="message">
                    [LAST_MSG_1]
                </div>
                <div class="message">
                    [LAST_MSG_2]
                </div>
                <div class="message">
                    [LAST_MSG_3]
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

        template = process_time_difference(template, category)

        let tipsMsgs = category["tips"].filter((tip) => {
            return tip["text"].length > 5
        })

        tipsMsgs.sort((tipa, tipb) => {
            return tipa["time"] - tipb["time"]
        })

        tipsMsgs.reverse()

        if (tipsMsgs.length > 0) {
            template = template.replace("[LAST_MSG_1]", '"' + tipsMsgs[0]["text"] + '"')
        } else {
            template = template.replace("[LAST_MSG_1]", "Submit more tips to fill this box!")
        }

        if (tipsMsgs.length > 1) {
            template = template.replace("[LAST_MSG_2]", '"' + tipsMsgs[1]["text"] + '"')
        } else {
            template = template.replace("[LAST_MSG_2]", "Submit more tips to fill this box!")
        }

        if (tipsMsgs.length > 2) {
            template = template.replace("[LAST_MSG_3]", '"' + tipsMsgs[2]["text"] + '"')
        } else {
            template = template.replace("[LAST_MSG_3]", "Submit more tips to fill this box!")
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

function process_time_difference(template, category) {
    tips = category["tips"]

    if (tips.length == 0) {
        return template.replace("[LAST_SUGGESTED_TIME]", "")
    }

    tips.sort((tipa, tipb) => {
            return tipa["time"] - tipb["time"]
        })

    tips.reverse()

    lastTime = tips[0]["time"]
    currentTime = new Date().getTime() / 1000

    difference = currentTime - lastTime

    if (difference < 60) {
        // Less than a minute has passed:
        output = `${Math.round(difference)} seconds ago`;
    } else if (difference < 3600) {
        // Less than an hour has passed:
        output = `${Math.floor(difference / 60)} minutes ago`;
    } else if (difference < 86400) {
        // Less than a day has passed:
        output = `${Math.floor(difference / 3600)} hours ago`;
    } else if (difference < 2620800) {
        // Less than a month has passed:
        output = `${Math.floor(difference / 86400)} days ago`;
    } else if (difference < 31449600) {
        // Less than a year has passed:
        output = `${Math.floor(difference / 2620800)} months ago`;
    } else {
        // More than a year has passed:
        output = `${Math.floor(difference / 31449600)} year(s) ago`;
    }

    return template.replace("[LAST_SUGGESTED_TIME]", "Last added to " + output)
}

setTimeout(function () {
    if (window.loaded) {
        return;
    }
    document.getElementById("loading-msg-here").innerHTML = '<p class="loading-msg" id="loading-msg">Loading</p>'
}, 300)