import puppeteer from 'puppeteer-extra';
import stealth from 'puppeteer-extra-plugin-stealth';
import { promises as fs } from 'fs';
import { user } from './auth.js';
puppeteer.use(stealth());

const sleep = (ms) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

async function cookie() {
  try {
    const browser = await puppeteer.launch({
      headless: false,
    });
    const page = await browser.newPage();
    await page.setViewport({
      width: 1366,
      height: 768,
    });
    await page.goto('https://www.myntra.com/login', {
      waitUntil: 'networkidle2',
    });
    await page.focus('.form-group .mobileNumberInput');
    await page.keyboard.type(user, { delay: 300 });
    await page.click('.mobileInputContainer .submitBottomOption');

    await page.waitForSelector('.otpContainer');
    const otp = await page.evaluate(() => {
      return prompt('Please enter the OTP:');
    });
    await page.keyboard.press(otp[0]);
    await page.keyboard.press(otp[1]);
    await page.keyboard.press(otp[2]);
    await page.keyboard.press(otp[3]);
    await page.waitForNavigation({
      waitUntil: 'networkidle2',
    });
    await sleep(10000);
    const cookies = await page.cookies();
    await fs.writeFile(
      '../cookies/cookies.json',
      JSON.stringify(cookies, null, 2)
    );
    await browser.close();
  } catch (error) {
    console.log(error);
  }
}
cookie();
