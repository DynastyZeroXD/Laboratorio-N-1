package JavaSelenium.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class InventoryPage extends BasePage {

    private final By addBackpackButton = By.id("add-to-cart-sauce-labs-backpack");
    private final By cartBadge = By.cssSelector("[data-test='shopping-cart-badge']");
    private final By cartLink = By.cssSelector("[data-test='shopping-cart-link']");

    public InventoryPage(WebDriver driver) {
        super(driver);
    }

    public InventoryPage addBackpackToCart() {
        click(addBackpackButton);
        return this;
    }

    public String getCartBadgeCount() {
        return getText(cartBadge);
    }

    public CartPage openCart() {
        click(cartLink);
        wait.until(driver -> driver.getCurrentUrl().contains("cart.html"));
        return new CartPage(driver);
    }
}
