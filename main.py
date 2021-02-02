import json
import requests


def get_info(course_id: str) -> dict:
    result = {"videoNum": "ERR", "videoTime": "ERR"}
    url = "http://mooc1.chaoxing.com/moocAnalysis/courseStatistic?courseId=" + course_id
    firefox = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/88.0.4324.96 Safari/537.36 "
    }
    try:
        resp = requests.get(url, headers=firefox)

        result["videoNum"] = resp.json()["videoNum"]
        result["videoTime"] = resp.json()["videoTime"]
    except (KeyError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError,
            ConnectionError) as ex:
        print(
            f"\n[ERROR]Error in getting class info, courseId:{course_id}, error message:{str(ex)}")

    return result


def get_classes() -> list:
    ret_list = []
    with open('./all.json') as data_file:
        data_json = json.load(data_file)
        data_count = len(data_json["data"])
        course_name = "UnKnow"
        
        # 计数变量
        i = 0
        while i < data_count:
            course_item = data_json["data"][i]
            i += 1
            course_name = course_item["name"]
            try:
                # 获取课程信息
                course_id = course_item["courseId"]
                course_info = get_info(course_id)
                # 校验获取信息是否成功
                if course_info["videoNum"] != "ERR" and course_info["videoTime"] != "ERR":

                    new_course_item = {
                        "name": course_name,
                        "link": f"http://mooc1.chaoxing.com/course/{course_id}.html",
                        "id": course_item["courseId"],
                        "videoTime": course_info["videoTime"],
                        "videoNum": course_info["videoNum"]
                    }
                    ret_list.append(new_course_item)
                    format_bar(i, data_count, new_course_item)

            except (
                    KeyError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError,
                    ConnectionError) as ex:
                print(
                    f"\n[ERROR]Error in get classes, courseName {course_name}, error message:{str(ex)}")

    return ret_list


output_str_length_last = 0


def format_bar(input_int_start: int, input_int_end, input_dict: dict) -> None:
    # 设置使用全局变量
    global output_str_length_last

    output_str = f"\r [{input_int_start}/{input_int_end}] 获取课程 {json.dumps(input_dict, ensure_ascii=False)} "
    output_str_length = len(output_str)
    print(output_str, end="")

    # 输出缓冲空格
    if output_str_length < output_str_length_last:
        i = 0
        while i <= output_str_length_last - output_str_length:
            print("  ", end="")
            i += 1

    output_str_length_last = output_str_length


def format_output(input_dict: dict) -> None:
    output_name = input_dict['name']
    output_num = input_dict['videoNum']
    output_time = input_dict['videoTime']
    output_page = input_dict['link']

    split_str1 = "\t\t"
    split_str2 = "\t\t"

    if len(output_name) >= 6:
        split_str1 = "\t"
    if int(output_time) >= 1000:
        split_str2 = "\t"

    print(f"课程:{output_name}{split_str1} | 视频数量:{output_num}\t | 视频时间:{output_time}{split_str2} | 页面:{output_page}")


if __name__ == '__main__':
    print("开始解析课程")
    data_list = get_classes()
    print("解析完成，开始排序")
    try:
        # 加reverse=True，利于控制台查看倒序
        data_list.sort(key=lambda this_list: this_list["videoTime"])
        print("排序完成，输出结果")
        for item in data_list:
            format_output(item)

    except KeyError as e:
        print("Error in sort!" + str(e))
