// Auto unfollow + Auto Scroll + Random auto scroll
// Human-like auto-unfollow for X (Twitter)

// Create a stop flag (so you can stop anytime with: window.stopUnfollow = true)
window.stopUnfollow = false;

function randomDelay(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function unfollowAll() {
    let count = 0;

    while (!window.stopUnfollow) {
        // Find unfollow buttons
        let buttons = Array.from(document.querySelectorAll("button[data-testid*='unfollow']"));

        if (buttons.length === 0) {
            console.log("⏳ No buttons found, scrolling like human...");
            window.scrollBy(0, randomDelay(600, 1200)); // random scroll distance
            await new Promise(r => setTimeout(r, randomDelay(2000, 4000))); // wait for load
            continue;
        }

        // Pick a random button from visible ones (not always the first)
        let btn = buttons[Math.floor(Math.random() * buttons.length)];
        btn.scrollIntoView({ behavior: "smooth", block: "center" });
        await new Promise(r => setTimeout(r, randomDelay(500, 1200)));

        // Click unfollow
        btn.click();
        count++;
        console.log("👋 Unfollowed", count, "accounts");

        // Handle confirm popup
        await new Promise(r => setTimeout(r, randomDelay(500, 1500)));
        let confirm = Array.from(document.querySelectorAll("span"))
            .find(el => el.innerText.trim() === "Unfollow");
        if (confirm) confirm.closest("button").click();

        // Wait a random delay before next action
        let waitTime = randomDelay(1500, 4000);
        console.log("⏳ Waiting", waitTime, "ms before next unfollow...");
        await new Promise(r => setTimeout(r, waitTime));

        // Occasionally take a "longer break"
        if (count % randomDelay(7, 12) === 0) {
            let longBreak = randomDelay(5000, 10000);
            console.log("😴 Taking a longer break for", longBreak, "ms...");
            await new Promise(r => setTimeout(r, longBreak));
        }
    }

    console.log("🛑 Stopped unfollow script after", count, "accounts");
}

unfollowAll();