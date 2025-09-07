// Auto unfollow + Auto Scroll + Random auto scroll + Stop after unfollowing 100
// =============================
// Human-like Auto Unfollow Script
// =============================

// Control flag (set to true to stop anytime)
window.stopUnfollow = false;

function randomDelay(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function unfollowSession(limit = 100) {  // 🔥 now 100 per session
    let count = 0;

    while (!window.stopUnfollow && count < limit) {
        let buttons = Array.from(document.querySelectorAll("button[data-testid*='unfollow']"));

        if (buttons.length === 0) {
            console.log("⏳ No unfollow buttons found, scrolling...");
            window.scrollBy(0, randomDelay(600, 1200));
            await new Promise(r => setTimeout(r, randomDelay(2000, 4000)));
            continue;
        }

        // Pick a random unfollow button
        let btn = buttons[Math.floor(Math.random() * buttons.length)];
        btn.scrollIntoView({ behavior: "smooth", block: "center" });
        await new Promise(r => setTimeout(r, randomDelay(500, 1200)));

        // Click unfollow
        btn.click();
        count++;
        console.log("👋 Unfollowed", count, "this session");

        // Confirm if needed
        await new Promise(r => setTimeout(r, randomDelay(500, 1500)));
        let confirm = Array.from(document.querySelectorAll("span"))
            .find(el => el.innerText.trim() === "Unfollow");
        if (confirm) confirm.closest("button").click();

        // Random short wait
        let waitTime = randomDelay(1500, 4000);
        console.log("⏳ Waiting", waitTime, "ms...");
        await new Promise(r => setTimeout(r, waitTime));

        // Occasional longer pauses (every 8–15 unfollows)
        if (count % randomDelay(8, 15) === 0) {
            let longBreak = randomDelay(5000, 12000);
            console.log("😴 Taking a long break:", longBreak, "ms...");
            await new Promise(r => setTimeout(r, longBreak));
        }
    }

    console.log("✅ Session complete:", count, "unfollows.");

    // Schedule next session if not stopped
    if (!window.stopUnfollow) {
        let cooldown = randomDelay(5 * 60 * 1000, 15 * 60 * 1000); // 5–15 min
        console.log("🛑 Cooling down for", Math.floor(cooldown / 60000), "minutes...");
        setTimeout(() => unfollowSession(limit), cooldown);
    }
}

// 🚀 Start automation (100 per session, auto resume)
unfollowSession(100);