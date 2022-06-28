from playwright.sync_api import Playwright, sync_playwright, expect
import time

nomes_alunos = ["TroyRogerJr", "Michel Martins Pereira"]
nomes_exercicios = ["E1T1"]


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.tinkercad.com/
    page.goto("https://www.tinkercad.com/")

    # Click text=Log In
    # with page.expect_navigation(url="https://www.tinkercad.com/login"):
    with page.expect_navigation():
        page.locator("text=Log In").click()

    # Click text=Personal accounts
    page.locator("text=Personal accounts").click()

    # Click a:has-text("Sign in with Google")
    # with page.expect_navigation(url="https://accounts.google.com/o/oauth2/v2/auth?client_id=364722000741-999vupl5mu2ldgg1cjqtajs03a4fjr4l.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Faccounts.autodesk.com%2Fsocial%2Fcallback&scope=openid%20email%20profile&state=googleplus.9918be24-c290-457e-a573-d9e5f9bc49c1&response_type=code&response_mode=form_post"):
    with page.expect_navigation():
        page.locator('a:has-text("Sign in with Google")').click()
    # expect(page).to_have_url("https://accounts.autodesk.com/Authentication/Landing?ReturnUrl=%2Fauthorize%3Fviewmode%3Diframe%26lang%3Den-US%26realm%3D%252A.tinkercad.com%26ctx%3Dtinkercad%26authtype%3Dsocialoradsk%26authviewmode%3Dredirect%26autologin%3Dtrue%26socialproviderpref%3DGO%26AuthKey%3Dc5607c32-9d7d-40c9-8ab4-91004be15640")

    # Click button:has-text("Próxima")
    # with page.expect_navigation(url="https://accounts.google.com/signin/v2/challenge/pwd?client_id=364722000741-999vupl5mu2ldgg1cjqtajs03a4fjr4l.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Faccounts.autodesk.com%2Fsocial%2Fcallback&scope=openid%20email%20profile&state=googleplus.9918be24-c290-457e-a573-d9e5f9bc49c1&response_type=code&response_mode=form_post&flowName=GeneralOAuthFlow&cid=1&navigationDirection=forward&TL=AM3QAYZwtAuQ5kLFVX_cxwjwVQUaAuLeHccuc_rDnHrINIvf2i2U8Fn4Vodorqim"):
    # with page.expect_navigation():
    #     page.locator('button:has-text("Próxima")').click()

    # # Click [aria-label="Digite sua senha"]
    # page.locator('[aria-label="Digite sua senha"]').click()

    # # Fill [aria-label="Digite sua senha"]
    # page.locator('[aria-label="Digite sua senha"]').fill("Tav2011&joia")

    # # Click button:has-text("Próxima")
    # # with page.expect_navigation(url="https://accounts.google.com/signin/v2/challenge/dp?client_id=364722000741-999vupl5mu2ldgg1cjqtajs03a4fjr4l.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Faccounts.autodesk.com%2Fsocial%2Fcallback&scope=openid%20email%20profile&state=googleplus.9918be24-c290-457e-a573-d9e5f9bc49c1&response_type=code&response_mode=form_post&flowName=GeneralOAuthFlow&cid=8&TL=AM3QAYZwtAuQ5kLFVX_cxwjwVQUaAuLeHccuc_rDnHrINIvf2i2U8Fn4Vodorqim&navigationDirection=forward"):
    # with page.expect_navigation():
    #     page.locator('button:has-text("Próxima")').click()
    # expect(page).to_have_url("https://accounts.google.com/signin/v2/challenge/pwd?client_id=364722000741-999vupl5mu2ldgg1cjqtajs03a4fjr4l.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Faccounts.autodesk.com%2Fsocial%2Fcallback&scope=openid%20email%20profile&state=googleplus.9918be24-c290-457e-a573-d9e5f9bc49c1&response_type=code&response_mode=form_post&flowName=GeneralOAuthFlow&cid=1&navigationDirection=forward&TL=AM3QAYZwtAuQ5kLFVX_cxwjwVQUaAuLeHccuc_rDnHrINIvf2i2U8Fn4Vodorqim")

    input()

    # Go to https://accounts.google.com.br/accounts/SetSID?ssdc=1&sidt=ALWU2cu3jou514Llsil6Wd5c09lYY/OnFj8rGw8mlyx5JOTrGE039JV8sVK6w%2BbLIBkHY5WEaXYmI2mHxnxmhzW9wMr5twfyC1gp2RKd6lpueERZE0pS905vEduoI7hXMhh4IGjFTJGjAXEKTLtnc%2BfVRCWjcGTNUoumLLVmd81OfX/ZwZWoKUC7h51TxHoN%2BFEFcIOa50ZI1jtTygqAQdVMvT3lDbu8XOVs8jqqLo2hmO0KEw10Gjmj/JEMlvhbWaugZh1Zz5I8CdfcWYhbTtIODXDvOA%2BKd5FuefeBGEdxoyqXFp6dO2dM27ZHG7Xo8xo6KvpucF8wfOIAWtxLIJcoslS9POwaFxM4bhxytw8XlCDFN5Dj8jAzrnTdOiWi3bRMbHWV/fzm1auY5H65w4%2BkWoo0Eo0tamzfd5EW4%2BYr0YfQmTl7HUmolpJId5EUyMWqC6spcxugzCQp8IcyVCmCRFm%2B3BgUdw%3D%3D&continue=https://accounts.google.com/signin/oauth/consent?authuser%3D0%26part%3DAJi8hAOtMGmTpu9taqO1RP18LZLYgxGNlQy8WTaeex0X_GBWl1d8vVNlq3D9Yp6QjvLEmTEeHQI57Vb7eeM4OI8Cdv1cBXja1LhMQOaZZbXoydplebJuH21EIlTpujz2SUPvkWuQaOHnUDfgMUcn7mVxjeXIA8cP1_mj_swCKjZyYd4_ABXeTKfQYAgJ9oRIXijAJM_YxpayNnaryjesH5w-8y2BM1JTcOHPbS8W7rybGo8JAkcwPR1Xf2ol4iU3xDijbSQmb0mmRm9a6JqpxR54jynBq-GD4zwE8xg8yrSCmjDrwsF76vhtvQPWWCHDxz-0f1T_VTEVUinfFWoglJfuf5AznWnYSm2P4kUWu_9K8iecJbyUWy3a_YZJqpW252-GD02w538Kd7StklPRVNm-3RjJR3BoP2DP2nVwPz1EhLRGpm4wnfPbAkwPyYeufSJ38qpA_OHv2V6ykVFv76UqCXtUkVpjrzHtZ_F5yyxS9QOSa3YGkdU%26as%3DS-754931786%253A1656428815562547%26rapt%3DAEjHL4OKctwBvb75a6wbkBRlh42Pq0fCXV0UmpWYHteUSdhQjQSE6exoAzDftZLJpQUc4YMYLp5ahsJc3Pshk8LLqt7tjsoo6w%23&tcc=1
    page.goto(
        "https://accounts.google.com.br/accounts/SetSID?ssdc=1&sidt=ALWU2cu3jou514Llsil6Wd5c09lYY/OnFj8rGw8mlyx5JOTrGE039JV8sVK6w%2BbLIBkHY5WEaXYmI2mHxnxmhzW9wMr5twfyC1gp2RKd6lpueERZE0pS905vEduoI7hXMhh4IGjFTJGjAXEKTLtnc%2BfVRCWjcGTNUoumLLVmd81OfX/ZwZWoKUC7h51TxHoN%2BFEFcIOa50ZI1jtTygqAQdVMvT3lDbu8XOVs8jqqLo2hmO0KEw10Gjmj/JEMlvhbWaugZh1Zz5I8CdfcWYhbTtIODXDvOA%2BKd5FuefeBGEdxoyqXFp6dO2dM27ZHG7Xo8xo6KvpucF8wfOIAWtxLIJcoslS9POwaFxM4bhxytw8XlCDFN5Dj8jAzrnTdOiWi3bRMbHWV/fzm1auY5H65w4%2BkWoo0Eo0tamzfd5EW4%2BYr0YfQmTl7HUmolpJId5EUyMWqC6spcxugzCQp8IcyVCmCRFm%2B3BgUdw%3D%3D&continue=https://accounts.google.com/signin/oauth/consent?authuser%3D0%26part%3DAJi8hAOtMGmTpu9taqO1RP18LZLYgxGNlQy8WTaeex0X_GBWl1d8vVNlq3D9Yp6QjvLEmTEeHQI57Vb7eeM4OI8Cdv1cBXja1LhMQOaZZbXoydplebJuH21EIlTpujz2SUPvkWuQaOHnUDfgMUcn7mVxjeXIA8cP1_mj_swCKjZyYd4_ABXeTKfQYAgJ9oRIXijAJM_YxpayNnaryjesH5w-8y2BM1JTcOHPbS8W7rybGo8JAkcwPR1Xf2ol4iU3xDijbSQmb0mmRm9a6JqpxR54jynBq-GD4zwE8xg8yrSCmjDrwsF76vhtvQPWWCHDxz-0f1T_VTEVUinfFWoglJfuf5AznWnYSm2P4kUWu_9K8iecJbyUWy3a_YZJqpW252-GD02w538Kd7StklPRVNm-3RjJR3BoP2DP2nVwPz1EhLRGpm4wnfPbAkwPyYeufSJ38qpA_OHv2V6ykVFv76UqCXtUkVpjrzHtZ_F5yyxS9QOSa3YGkdU%26as%3DS-754931786%253A1656428815562547%26rapt%3DAEjHL4OKctwBvb75a6wbkBRlh42Pq0fCXV0UmpWYHteUSdhQjQSE6exoAzDftZLJpQUc4YMYLp5ahsJc3Pshk8LLqt7tjsoo6w%23&tcc=1"
    )

    # Go to https://accounts.google.com.br/accounts/SetSID
    page.goto("https://accounts.google.com.br/accounts/SetSID")

    # Go to https://accounts.google.com/signin/oauth/consent?authuser=0&part=AJi8hAOtMGmTpu9taqO1RP18LZLYgxGNlQy8WTaeex0X_GBWl1d8vVNlq3D9Yp6QjvLEmTEeHQI57Vb7eeM4OI8Cdv1cBXja1LhMQOaZZbXoydplebJuH21EIlTpujz2SUPvkWuQaOHnUDfgMUcn7mVxjeXIA8cP1_mj_swCKjZyYd4_ABXeTKfQYAgJ9oRIXijAJM_YxpayNnaryjesH5w-8y2BM1JTcOHPbS8W7rybGo8JAkcwPR1Xf2ol4iU3xDijbSQmb0mmRm9a6JqpxR54jynBq-GD4zwE8xg8yrSCmjDrwsF76vhtvQPWWCHDxz-0f1T_VTEVUinfFWoglJfuf5AznWnYSm2P4kUWu_9K8iecJbyUWy3a_YZJqpW252-GD02w538Kd7StklPRVNm-3RjJR3BoP2DP2nVwPz1EhLRGpm4wnfPbAkwPyYeufSJ38qpA_OHv2V6ykVFv76UqCXtUkVpjrzHtZ_F5yyxS9QOSa3YGkdU&as=S-754931786%3A1656428815562547&rapt=AEjHL4OKctwBvb75a6wbkBRlh42Pq0fCXV0UmpWYHteUSdhQjQSE6exoAzDftZLJpQUc4YMYLp5ahsJc3Pshk8LLqt7tjsoo6w#
    page.goto(
        "https://accounts.google.com/signin/oauth/consent?authuser=0&part=AJi8hAOtMGmTpu9taqO1RP18LZLYgxGNlQy8WTaeex0X_GBWl1d8vVNlq3D9Yp6QjvLEmTEeHQI57Vb7eeM4OI8Cdv1cBXja1LhMQOaZZbXoydplebJuH21EIlTpujz2SUPvkWuQaOHnUDfgMUcn7mVxjeXIA8cP1_mj_swCKjZyYd4_ABXeTKfQYAgJ9oRIXijAJM_YxpayNnaryjesH5w-8y2BM1JTcOHPbS8W7rybGo8JAkcwPR1Xf2ol4iU3xDijbSQmb0mmRm9a6JqpxR54jynBq-GD4zwE8xg8yrSCmjDrwsF76vhtvQPWWCHDxz-0f1T_VTEVUinfFWoglJfuf5AznWnYSm2P4kUWu_9K8iecJbyUWy3a_YZJqpW252-GD02w538Kd7StklPRVNm-3RjJR3BoP2DP2nVwPz1EhLRGpm4wnfPbAkwPyYeufSJ38qpA_OHv2V6ykVFv76UqCXtUkVpjrzHtZ_F5yyxS9QOSa3YGkdU&as=S-754931786%3A1656428815562547&rapt=AEjHL4OKctwBvb75a6wbkBRlh42Pq0fCXV0UmpWYHteUSdhQjQSE6exoAzDftZLJpQUc4YMYLp5ahsJc3Pshk8LLqt7tjsoo6w#"
    )

    # Go to https://accounts.autodesk.com/authorize?viewmode=iframe&lang=en-US&realm=%2A.tinkercad.com&ctx=tinkercad&authtype=socialoradsk&authviewmode=redirect&autologin=true&socialproviderpref=GO&AuthKey=c5607c32-9d7d-40c9-8ab4-91004be15640&source=soc&Provider=googleplus
    page.goto(
        "https://accounts.autodesk.com/authorize?viewmode=iframe&lang=en-US&realm=%2A.tinkercad.com&ctx=tinkercad&authtype=socialoradsk&authviewmode=redirect&autologin=true&socialproviderpref=GO&AuthKey=c5607c32-9d7d-40c9-8ab4-91004be15640&source=soc&Provider=googleplus"
    )

    # Go to https://www.tinkercad.com/
    page.goto("https://www.tinkercad.com/")

    # Go to https://www.tinkercad.com/dashboard
    page.goto("https://www.tinkercad.com/dashboard")

    # Click text=Classes
    page.locator("text=Classes").click()
    # expect(page).to_have_url("https://www.tinkercad.com/dashboard?type=classes")

    # Click a[role="button"]:has-text("2022.1 Computação 1 - IF71A")
    # with page.expect_navigation(url="https://www.tinkercad.com/classrooms/cNhyXcecgXF"):
    with page.expect_navigation():
        page.locator('a[role="button"]:has-text("2022.1 Computação 1 - IF71A")').click()

    for nome in nomes_alunos:
        # Click text=Michel Martins Pereira
        # with page.expect_navigation(url="https://www.tinkercad.com/users/2wyyms6dso8-michel-martins-pereira"):
        with page.expect_navigation():
            page.locator(f"text={nome}").click()
        # expect(page).to_have_url("https://www.tinkercad.com/users/2wyyms6dso8-michel-martins-pereira")

        # Click #content >> text=Circuits
        page.locator("#content >> text=Circuits").click()
        # expect(page).to_have_url("https://www.tinkercad.com/users/2wyyms6dso8-michel-martins-pereira?category=circuits&sort=likes&view_mode=default")

        for exercicio in nomes_exercicios:
            # Click text=Tinker thisE1T13 months agoPrivate0 >> div >> nth=1
            page.locator(f'a:has-text("{exercicio}")').nth(1).click()
            # expect(page).to_have_url("https://www.tinkercad.com/things/8yVAV3groYD-e1t1")

            # Click a:has-text("Simulate")
            page.locator('a:has-text("Simulate")').click()

            # Click text=Code >> nth=0
            page.frame_locator(
                "text=Add an image of this Thing JPG, GIF or PNG image that is under 5MB UploadSimulat >> iframe"
            ).locator("text=Code").first.click()

            # Click .circ_btn__icon.cio-ui-icon > svg >> nth=0
            with page.expect_download() as download_info:
                page.frame_locator(
                    "text=Add an image of this Thing JPG, GIF or PNG image that is under 5MB UploadSimulat >> iframe"
                ).locator(".circ_btn__icon.cio-ui-icon > svg").first.click()
            download = download_info.value

            time.sleep(2)

            print(f"Download path: {download.path()}")

            print("Saving to Dwonloads folder...")
            download.save_as(f'{nome.replace(" ", "")}_{exercicio}.ino')

            time.sleep(2)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
