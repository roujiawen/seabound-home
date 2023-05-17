import html
import json

def generate_team():

    def generate_item(animation_delay, linkedin, image, name, title):
        item_template = """<div class="col-lg-3 col-md-5 col-sm-6" data-aos="fade-down" data-aos-delay="{}">
            <a href="{}" target="_blank">
                <img src="{}" style="width:60%;" alt="" class="img-fluid rounded-circle mb-6">
            </a>
            <h5 class="mb-2 text-light-1">
                {}
            </h5>
            <p class="mb-12 text-light-2">
                {}
            </p>
        </div>""".format(animation_delay, linkedin, image, html.escape(name), html.escape(title))
        return item_template

    with open("data.json") as f:
        json_data = json.load(f)
    animation_delays = [150, 250, 400, 500, 250, 400, 500, 650, 400, 500, 650, 750, 500, 650, 750, 900]
    if len(animation_delays) < len(json_data["team"]):
        animation_delays += [900] * (len(json_data["team"]) - len(animation_delays))

    items_buffer = []
    for delay, data in zip(animation_delays, json_data["team"]):
        items_buffer.append(generate_item(delay, data["linkedin"], data["image"], data["name"], data["title"]))
    items = "\n".join(items_buffer)

    with open('team-template.html') as f:
        team_template = f.read()

    team_template = team_template.replace("{{{items}}}", items)
    return team_template

def generate_jobs():

    def generate_item(animation_delay, job_title, subtext, url, open_in_new_tab, action_text):
        if open_in_new_tab:
            tab_html_code = 'target="_blank"'
        else:
            tab_html_code = ""
        item_template = """<div class="mb-8 col-sm-8 col-md-7 col-lg-4 d-flex" data-aos="fade" data-aos-delay="{}">
            <div class="w-100 p-8 p-md-16 bg-bg-3 p-xl-10 p-xxl-16 p-lg-3 py-lg-4">
                <h4 class="" placeholder="">
                    {}
                </h4>
                <p class="my-4 text-2">
                    {}
                </p>
                <a href="{}" {}
                    class="fw-bold btn w-80 btn-action-2 text-light-1">
                    {}
                </a>
            </div>
        </div>""".format(animation_delay, html.escape(job_title), html.escape(subtext), url, tab_html_code, html.escape(action_text))
        return item_template

    with open("data.json") as f:
        json_data = json.load(f)

    animation_delays = [250, 400, 500, 400, 500, 650, 500, 650, 750, 650, 750, 900]
    if len(animation_delays) < len(json_data["team"]):
        animation_delays += [900] * (len(json_data["team"]) - len(animation_delays))

    items_buffer = []
    for delay, data in zip(animation_delays, json_data["jobs"]):
        items_buffer.append(generate_item(delay, data["job_title"], data["subtext"], data["url"], data["open_in_new_tab"], data["action_text"]))
    items = "\n".join(items_buffer)

    with open('jobs-template.html') as f:
        jobs_template = f.read()

    jobs_template = jobs_template.replace("{{{items}}}", items)
    return jobs_template

def generate_news():
    def generate_item(col, url, image, date, headline):
        if col == "column1":
            item_template = """
            <!-- Press Item Column 1 Big -->
            <div>
                <a href="{}" target="_blank">
                    <img src="{}" alt="" class="w-100 mb-4">
    					</a>
    					<p class="mb-2 text-light-1">
                        {}
    					</p>
    					<h2 class="mb-2 text-light-1">
    					{}
    					</h2>
    					<a href="{}" target="_blank" class="text-action-7 fw-bold">
    					Read more
    					</a>
            </div>""".format(url, image, html.escape(date), html.escape(headline), url)
            return item_template
        elif col == "column2":
            item_template = """
            <!-- Press Item Column 2 -->
            <div>
                <a href="{}" target="_blank">
                    <img src="{}" alt="" class="w-100 mb-4">
                </a>
                <p class="mb-2 text-light-1">
                    {}
                </p>
                <h5 class="mb-4 mb-sm-10 text-light-1">
                    {}
                </h5>
                <a href="{}"
                    target="_blank" class="text-action-7 fw-bold">
                    Read more
                </a>
                <div class="mt-8 mb-15 border-bottom opacity-20 border-light-1">
                </div>
            </div>""".format(url, image, html.escape(date), html.escape(headline), url)
            return item_template
        elif col == "column3":
            item_template = """
            <!-- Press Item Column 3 -->
            <div>
                <a href="{}" target="_blank">
                    <img src="{}" alt="" class="w-100 mb-4">
                </a>
                <p class="mb-2 text-light-1">
                    {}
                </p>
                <h5 class="mb-4 mb-sm-10 text-light-1">
                    {}
                </h5>
                <a href="{}"
                    target="_blank" class="text-action-7 fw-bold">
                    Read more
                </a>
                <div class="mt-8 mb-15 border-bottom opacity-20 border-light-1">
                </div>
            </div>""".format(url, image, html.escape(date), html.escape(headline), url)
            return item_template
        else:
            return ""

    with open("data.json") as f:
        json_data = json.load(f)

    columns = []
    for col in ["column1", "column2", "column3"]:
        items_buffer = []
        for data in json_data["news"][col]:
            items_buffer.append(generate_item(col, data["url"], data["image"], data["date"], data["headline"]))
        items = "\n".join(items_buffer)
        columns.append(items)

    with open('news-template.html') as f:
        news_template = f.read()

    news_template = news_template.replace("{{{column1_items}}}", columns[0])
    news_template = news_template.replace("{{{column2_items}}}", columns[1])
    news_template = news_template.replace("{{{column3_items}}}", columns[2])
    return news_template

with open('template.html') as f:
    template = f.read()

replace_dict = {
    "{{{team}}}": generate_team(),
    "{{{jobs}}}": generate_jobs(),
    "{{{news}}}": generate_news()
}

for old, new in replace_dict.items():
    template = template.replace(old, new)

with open('index.html', "w") as f:
    f.write(template)
