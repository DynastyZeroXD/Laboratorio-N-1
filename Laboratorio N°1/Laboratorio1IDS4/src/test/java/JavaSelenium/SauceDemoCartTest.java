package JavaSelenium;

import JavaSelenium.pages.CartPage;
import JavaSelenium.pages.InventoryPage;
import JavaSelenium.pages.LoginPage;
import io.qameta.allure.Description;
import io.qameta.allure.Feature;
import io.qameta.allure.Step;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

@Feature("Carrito de compras")
public class SauceDemoCartTest {

    private WebDriver driver;

    @BeforeEach
    void setUp() {
        driver = new ChromeDriver();
    }

    @Test
    @Description("Agrega un producto al carrito y valida que el carrito tenga exactamente un producto.")
    void shouldAddOneProductToCart() {
        LoginPage loginPage = new LoginPage(driver).open();
        InventoryPage inventoryPage = loginWithValidCredentials(loginPage);

        inventoryPage.addBackpackToCart();
        Assertions.assertEquals("1", inventoryPage.getCartBadgeCount(),
                "El indicador del carrito debe mostrar 1 producto.");

        CartPage cartPage = inventoryPage.openCart();

        Assertions.assertEquals(1, cartPage.getProductCount(),
                "El carrito debe contener exactamente un producto.");
        Assertions.assertTrue(cartPage.containsProduct("Sauce Labs Backpack"),
                "El producto agregado debe aparecer en el carrito.");
    }

    @Step("Iniciar sesión con un usuario válido")
    private InventoryPage loginWithValidCredentials(LoginPage loginPage) {
        return loginPage.loginAs("standard_user", "secret_sauce");
    }

    @AfterEach
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
