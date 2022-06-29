from playwright.sync_api import Playwright, sync_playwright, expect
from typing import List
import time


def run(
    playwright: Playwright, student_list: List[str], assigment_list: List[str]
) -> None:
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context(viewport={"width": 1600, "height": 1200})

    # Open new page
    page = context.new_page()

    print("Opening TinkerCAD...")
    # Go to https://www.tinkercad.com/
    page.goto("https://www.tinkercad.com/")

    # Click text=Log In
    # with page.expect_navigation(url="https://www.tinkercad.com/login"):
    print("Opening LogIn...")
    with page.expect_navigation():
        page.locator("text=Log In").click()

    # Click text=Personal accounts
    print("Opening Personal Accounts...")
    page.locator("text=Personal accounts").click()

    # Click a:has-text("Email or Username")

    print("Opening Enter Email...")
    with page.expect_navigation():
        page.locator('a:has-text("Email or Username")').click()

    # Fill input[name="UserName"]
    page.locator('input[name="UserName"]').fill("paulo@paulourbano.com")

    # Click [aria-label="Next button"]

    print("Opening Password...")
    with page.expect_navigation():
        page.locator('[aria-label="Next button"]').click()

    # Click [aria-label="Password text field"]
    page.locator('[aria-label="Password text field"]').click()

    # Fill [aria-label="Password text field"]
    page.locator('[aria-label="Password text field"]').fill("TinkerCAD2022")

    # Click [aria-label="Sign in button"]
    # with page.expect_navigation(url="https://www.tinkercad.com/dashboard"):
    print("Opening Submit...")
    with page.expect_navigation():
        page.locator('[aria-label="Sign in button"]').click()

    # Click a[role="button"]:has-text("2022.1 Computação 1 - IF71A")
    # with page.expect_navigation(url="https://www.tinkercad.com/classrooms/cNhyXcecgXF"):
    print("Opening Classroom...")
    with page.expect_navigation():
        page.locator('a[role="button"]:has-text("2022.1 Computação 1 - IF71A")').click()

    for current_student in student_list:
        print(f"{current_student=}")
        page.goto("https://www.tinkercad.com/classrooms/cNhyXcecgXF")

        with page.expect_navigation():
            page.locator(f"text={current_student}").click()

        page.locator("#content >> text=Circuits").click()

        for current_assigment in assigment_list:
            print(f"{current_assigment=}")
            # Click h3:has-text("E1T1")
            page.locator(f'h3:has-text("{current_assigment}")').click()

            # Click a:has-text("Simulate")
            page.locator('a:has-text("Simulate")').click()

            page.locator('a:has-text("Code")').first.click()

            with page.expect_download() as download_info:
                page.frame_locator(
                    "text=Add an image of this Thing JPG, GIF or PNG image that is under 5MB UploadSimulat >> iframe"
                ).locator(".circ_btn__icon.cio-ui-icon > svg").first.click()
            download = download_info.value

            saved_download_file = (
                f'{current_student.replace(" ", "")}_{current_assigment}.ino'
            )
            print(f"Saving {saved_download_file}...\n")
            download.save_as(saved_download_file)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright, ["Michel Martins Pereira", "TroyRogerJr"], ["E1T1"])

    # # Click a:has-text("Code") >> nth=0
    # page.frame_locator("text=Add an image of this Thing JPG, GIF or PNG image that is under 5MB UploadSimulat >> iframe").locator("a:has-text(\"Code\")").first.click()
    # # Click .circ_btn.circ_btn--m_icon >> nth=0
    # with page.expect_download() as download_info:
    #     page.frame_locator("text=Add an image of this Thing JPG, GIF or PNG image that is under 5MB UploadSimulat >> iframe").locator(".circ_btn.circ_btn--m_icon").first.click()
    # download = download_info.value
