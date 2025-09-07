// Same to auto unfollow but with auto scroll feature
// Auto-scroll + auto-unfollow for X (Twitter)

let delay = 1500; // ms between unfollows
let scrollDelay = 2000; // ms between scrolls
let count = 0;

async function unfollowAll() {
    while (true) {
        // Collect buttons on screen
        let buttons = Array.from(document.querySelectorAll("button[data-testid*='unfollow']"));
        
        if (buttons.length === 0) {
            console.log("⏳ No more unfollow buttons found, scrolling...");
            window.scrollBy(0, 1000); // scroll down
            await new Promise(r => setTimeout(r, scrollDelay));
            // Check again
            buttons = Array.from(document.querySelectorAll("button[data-testid*='unfollow']"));
            if (buttons.length === 0) {
                console.log("✅ Done! No more accounts to unfollow.");
                break;
            }
        }

        // Click first button
        let btn = buttons[0];
        btn.click();
        count++;
        console.log("⏳ Unfollowed", count, "accounts");

        // Confirm popup if needed
        await new Promise(r => setTimeout(r, 500));
        let confirm = Array.from(document.querySelectorAll("span"))
            .find(el => el.innerText.trim() === "Unfollow");
        if (confirm) confirm.closest("button").click();

        // Wait before next
        await new Promise(r => setTimeout(r, delay));
    }
}

unfollowAll();