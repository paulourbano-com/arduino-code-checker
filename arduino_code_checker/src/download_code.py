import traceback
import time
import configparser
from playwright.sync_api import Playwright, sync_playwright, expect
from typing import List, Optional
import os
import sys
import shutil
import datetime
from urllib.parse import urlparse


def run(
    playwright: Playwright,
    classroom_url: str,
    user: str,
    password: str,
    assigment_list: List[str],
    student_list: Optional[List[str]] = [],
    download_folder: str = "tinkercad_downloads",
    headless: bool = False,
) -> None:
    tinkercad_url = "https://www.tinkercad.com"

    download_folder = f"{download_folder}_{datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')}"

    if os.path.isdir(download_folder):
        shutil.rmtree(download_folder)

    os.mkdir(download_folder)

    browser = playwright.firefox.launch(headless=headless)
    context = browser.new_context(viewport={"width": 1600, "height": 1200})

    # Open new page
    page = context.new_page()

    print("Opening TinkerCAD...")
    page.goto("https://www.tinkercad.com/")

    print("Opening LogIn...")
    with page.expect_navigation():
        page.locator("text=Log In").click()

    print("Opening Personal Accounts...")
    page.locator("text=Personal accounts").click()

    print("Opening Enter Email...")
    with page.expect_navigation():
        page.locator('a:has-text("Email or Username")').click()

    page.locator('input[name="UserName"]').fill(user)

    print("Opening Password...")
    with page.expect_navigation():
        page.locator('[aria-label="Next button"]').click()

    page.locator('[aria-label="Password text field"]').click()

    page.locator('[aria-label="Password text field"]').fill(password)

    print("Opening Submit...")
    with page.expect_navigation():
        page.locator('[aria-label="Sign in button"]').click()

    print("Opening Classroom...")
    with page.expect_navigation():
        page.locator('a[role="button"]:has-text(" ")').first.wait_for()

    retries = 3
    while len(student_list) == 0 and retries > 0:
        try:
            page.goto(classroom_url)
            with page.expect_navigation():
                locator = page.locator("//span[contains(@class, 'name ng-star-inserted')]")
            locator.nth(0).wait_for(timeout=10000)

            count_rows = locator.count()

            student_list = []
            for index in range(count_rows):
                student_name = locator.nth(index).inner_text()
                # student_list.append(student_name)

                student_href = locator.nth(index).locator("//a").get_attribute("href")

                student_id = student_href.split("/")
                if len(student_id) > 0:
                    student_id = student_id[-1].split("?")[0]
                    
                student_list.append((student_name, student_href, student_id))
        except Exception as e:
            print(traceback.format_exc())
            retries = retries - 1

    print(f"{student_list=}")

    # sys.exit(0)
    student_list_file = os.path.join(
        download_folder,
        "student_list.txt",
    )

    for current_student in student_list:
        if len(current_student) == 0:
            continue

        print(f"\n{current_student[0]=}")

        with page.expect_navigation():
            page.goto(tinkercad_url + current_student[1])
            # input("Got to student page")
            
        map_circuit_name_url = {}
        try:
            page.locator("#content >> text=Circuits").click()
            time.sleep(2)
            all_results = page.locator("//a[contains(@class, 'ng-star-inserted')]")

            for result in all_results.all():
                circuit_name = result.inner_text()
                circuit_url = result.get_attribute("href")
                if len(circuit_name) > 0:
                    print("\n", circuit_name, " | ", circuit_url)
                    map_circuit_name_url[circuit_name] = circuit_url

            # input("Results for student")
        except Exception:
            print(traceback.format_exc())

        for circuit_name in map_circuit_name_url.keys():
            
            for current_assigment in assigment_list:
                if current_assigment not in circuit_name:
                    continue
                
                retries = 3
                success = False
                
                print(current_student[0], current_assigment, circuit_name)
                
                source_file = os.path.join(
                    download_folder,
                    f"{current_student[2]}_{current_assigment}_code.ino",
                )
                pcb_file = os.path.join(
                    download_folder,
                    f"{current_student[2]}_{current_assigment}_circuit.brd",
                )

                while retries > 0 and not success:

                    try:

                        page.goto(tinkercad_url + map_circuit_name_url.get(circuit_name))
                    
                        page.goto(f"{page.url}/editel")

                        page.locator("#CODE_EDITOR_ID >> text=Code").click()

                        with page.expect_download() as download_info:
                            page.locator(".circ_btn.circ_btn--m_icon").first.click()
                        
                        download = download_info.value
                        download.save_as(source_file)
                    
                        print(f"\t\tSaving {source_file}...")

                        page.locator("text=Send To").click()

                        with page.expect_download() as download_info:
                            page.locator("text=.BRD").nth(1).click()
                        
                        download = download_info.value
                        download.save_as(pcb_file)
                    
                        print(f"\t\tSaving {pcb_file}...\n")

                    
                        with open(student_list_file, "a", encoding="utf-8") as file_handle:
                            file_handle.write(f"{current_student[0].title()},{current_student[2]}\n")

                        success = True

                    except Exception:
                        print(traceback.format_exc())
                        retries -= retries

                    
                    # try:
                    #     with page.expect_navigation():
                    #         # page.locator(f"text={current_student}").click()
                    #         complete_name = page.locator(
                    #             f'a:has-text("{current_student}")'
                    #         ).first.inner_text()

                    #         page.locator(f'a:has-text("{current_student}")').first.click()

                    #     page.locator("#content >> text=Circuits").click()

                    #     base_page = page.url
                    #     unique_name = complete_name
                    #     try:
                    #         unique_name = urlparse(base_page).path.split("/")[2]
                    #     except:
                    #         print(traceback.format_exc())

                    #     with open(student_list_file, "a", encoding="utf-8") as file_handle:
                    #         file_handle.write(f"{complete_name.title()},{unique_name}\n")

                    #     # all_results = page.get_by_text(current_assigment, exact=False)
                    #     all_results = page.locator(f"a[href]:has-text('{current_assigment}')")
                    #     all_results.nth(0).wait_for(timeout=3000)

                    #     source_file = os.path.join(
                    #         download_folder,
                    #         f"{unique_name}_{current_assigment}_code.ino",
                    #     )
                    #     pcb_file = os.path.join(
                    #         download_folder,
                    #         f"{unique_name}_{current_assigment}_circuit.brd",
                    #     )


                    #     page.goto(tinkercad_url + all_results.first.get_attribute("href"))
                    
                    #     page.goto(f"{page.url}/editel")

                    #     page.locator("#CODE_EDITOR_ID >> text=Code").click()

                    #     with page.expect_download() as download_info:
                    #         page.locator(".circ_btn.circ_btn--m_icon").first.click()
                    #     download = download_info.value
                    #     download.save_as(source_file)
                    #     print(f"\t\tSaving {source_file}...")

                    #     page.locator("text=Send To").click()

                    #     with page.expect_download() as download_info:
                    #         page.locator("text=.BRD").nth(1).click()
                    #     download = download_info.value
                    #     download.save_as(pcb_file)
                    #     print(f"\t\tSaving {pcb_file}...\n")

                    #     page.goto(base_page)
                    #     page.locator(f"a[href]:has-text('{current_assigment}')").wait_for()
                    #     success = True
                    # except:
                    #     print(traceback.format_exc())
                    #     retries = retries - 1

        # continue

        # for current_assigment in assigment_list:
        #     retries = 3
        #     success = False

        #     while retries > 0 and not success:
        #         print(f"\t{current_assigment=}")

        #         page.goto(classroom_url)

        #         try:
        #             with page.expect_navigation():
        #                 # page.locator(f"text={current_student}").click()
        #                 complete_name = page.locator(
        #                     f'a:has-text("{current_student}")'
        #                 ).first.inner_text()

        #                 page.locator(f'a:has-text("{current_student}")').first.click()

        #             page.locator("#content >> text=Circuits").click()

        #             base_page = page.url
        #             unique_name = complete_name
        #             try:
        #                 unique_name = urlparse(base_page).path.split("/")[2]
        #             except:
        #                 print(traceback.format_exc())

        #             with open(student_list_file, "a", encoding="utf-8") as file_handle:
        #                 file_handle.write(f"{complete_name.title()},{unique_name}\n")

        #             # all_results = page.get_by_text(current_assigment, exact=False)
        #             all_results = page.locator(f"a[href]:has-text('{current_assigment}')")
        #             all_results.nth(0).wait_for(timeout=3000)

        #             source_file = os.path.join(
        #                 download_folder,
        #                 f"{unique_name}_{current_assigment}_code.ino",
        #             )
        #             pcb_file = os.path.join(
        #                 download_folder,
        #                 f"{unique_name}_{current_assigment}_circuit.brd",
        #             )


        #             page.goto(tinkercad_url + all_results.first.get_attribute("href"))
                    
        #             page.goto(f"{page.url}/editel")

        #             page.locator("#CODE_EDITOR_ID >> text=Code").click()

        #             with page.expect_download() as download_info:
        #                 page.locator(".circ_btn.circ_btn--m_icon").first.click()
        #             download = download_info.value
        #             download.save_as(source_file)
        #             print(f"\t\tSaving {source_file}...")

        #             page.locator("text=Send To").click()

        #             with page.expect_download() as download_info:
        #                 page.locator("text=.BRD").nth(1).click()
        #             download = download_info.value
        #             download.save_as(pcb_file)
        #             print(f"\t\tSaving {pcb_file}...\n")

        #             page.goto(base_page)
        #             page.locator(f"a[href]:has-text('{current_assigment}')").wait_for()
        #             success = True
        #         except:
        #             print(traceback.format_exc())
        #             retries = retries - 1

    context.close()
    browser.close()

    return download_folder


if __name__ == "__main__":
    start = datetime.datetime.now()

    parser = configparser.ConfigParser()
    parser.read(sys.argv[1])

    try:
        student_list = parser["tinkercad"]["students"].replace(" ", "").split(",")
        if len(student_list) == 1 and len(student_list[0]) == 0:
            student_list = []
    except KeyError:
        student_list = []

    try:
        headless = parser["tinkercad"].getboolean("headless")
    except KeyError:
        headless = True

    with sync_playwright() as playwright:
        run(
            playwright,
            classroom_url=parser["tinkercad"]["classroom"],
            user=parser["tinkercad"]["user"],
            password=parser["tinkercad"]["password"],
            student_list=student_list,
            assigment_list=parser["tinkercad"]["questions"].replace(" ", "").split(","),
            headless=headless,
        )
    end = datetime.datetime.now()
    print(f"Time elapsed: {end - start}s")
