import traceback
from playwright.sync_api import Playwright, sync_playwright, expect
from typing import List
import os
import shutil
import datetime


def run(
    playwright: Playwright,
    student_list: List[str],
    assigment_list: List[str],
    download_folder: str = "tinkercad_downloads",
) -> None:

    if os.path.isdir(download_folder):
        shutil.rmtree(download_folder)

    os.mkdir(download_folder)

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
        print(f"\n{current_student=}")
        # page.goto("https://www.tinkercad.com/classrooms/cNhyXcecgXF")

        # with page.expect_navigation():
        #     page.locator(f"text={current_student}").click()

        # page.locator("#content >> text=Circuits").click()

        for current_assigment in assigment_list:
            retries = 3
            success = False

            while retries > 0 and not success:
                print(f"\t{current_assigment=}")

                source_file = os.path.join(
                    download_folder,
                    f'{current_student.replace(" ", "")}_{current_assigment}_code.ino',
                )
                pcb_file = os.path.join(
                    download_folder,
                    f'{current_student.replace(" ", "")}_{current_assigment}_circuit.brd',
                )

                page.goto("https://www.tinkercad.com/classrooms/cNhyXcecgXF")

                try:
                    with page.expect_navigation():
                        page.locator(f"text={current_student}").click()

                    page.locator("#content >> text=Circuits").click()

                    all_results = page.locator(f'h3:has-text("{current_assigment}")')
                    all_results.nth(0).wait_for()

                    results_count = all_results.count()

                    # print(results_count)

                    base_page = page.url

                    for index in range(results_count):
                        # page.locator(f'h3:has-text("{current_assigment}")').click()
                        if results_count > 1:
                            source_file = os.path.join(
                                download_folder,
                                f'{current_student.replace(" ", "")}_{current_assigment}-{str(index+1).zfill(2)}_code.ino',
                            )
                            pcb_file = os.path.join(
                                download_folder,
                                f'{current_student.replace(" ", "")}_{current_assigment}-{str(index+1).zfill(2)}_circuit.brd',
                            )

                        all_results.nth(index).click()

                        page.goto(f"{page.url}/editel")

                        page.locator("#CODE_EDITOR_ID >> text=Code").click()

                        # Click .circ_btn.circ_btn--m_icon >> nth=0
                        with page.expect_download() as download_info:
                            page.locator(".circ_btn.circ_btn--m_icon").first.click()
                        download = download_info.value
                        download.save_as(source_file)
                        print(f"\t\tSaving {source_file}...")

                        # Click text=Send To
                        page.locator("text=Send To").click()

                        # Click text=.BRD >> nth=1
                        with page.expect_download() as download_info:
                            page.locator("text=.BRD").nth(1).click()
                        download = download_info.value
                        download.save_as(pcb_file)
                        print(f"\t\tSaving {pcb_file}...\n")

                        page.goto(base_page)
                        page.locator(f'h3:has-text("{current_assigment}")').nth(
                            0
                        ).wait_for()
                except:
                    print(traceback.format_exc())
                    retries = retries - 1

                success = True

    # ---------------------
    context.close()
    browser.close()


start = datetime.datetime.now()
with sync_playwright() as playwright:
    run(
        playwright,
        [
            # "Michel Martins Pereira",
            # "TroyRogerJr",
            # "tarekhenrique",
            # "MURILO JOSE IGNACIO",
            # "noamserique",
            # "Luiz Miguel Nascimento",
            # "Murilo Ignácio",
            # "JuliaValderes",
            # "viniciusrolim",
            # "thaispercebon",
            # "VINICIUS FERREIRA PINTO DE OLIVEIRA",
            # "Paulo Kupczak",
            # "Rafael Ferraz de Campos",
            # "luiza.2022",
            # "WILLIAM AMORIM DA COSTA",
            # "RAFAEL MURILO CHAMPINI",
            "JUAN VITOR MACANHAO CASIMIRO",
        ],
        ["E1T1"],  # , "E1T2", "E2T1", "E2T2", "E3T1"],
    )
end = datetime.datetime.now()
print(f"Time elapsed: {end - start}s")
