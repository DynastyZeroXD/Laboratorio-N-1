package JavaSelenium.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;

public class CartPage extends BasePage {

    private final By cartItems = By.cssSelector(".cart_item");
    private final By cartContents = By.id("cart_contents_container");

    public CartPage(WebDriver driver) {
        super(driver);
        find(cartContents);
    }

    public int getProductCount() {
        return driver.findElements(cartItems).size();
    }

    public boolean containsProduct(String productName) {
        List<String> names = driver.findElements(By.cssSelector("[data-test='inventory-item-name']"))
                .stream()
                .map(element -> element.getText().trim())
                .toList();
        return names.contains(productName);
    }
}
