from decimal import Decimal

from database import Base, engine
from crud import (
    create_category,
    create_product,
    create_stock_movement,
    create_supplier,
    deactivate_product,
    deactivate_supplier,
    get_all_categories,
    get_all_products,
    get_all_stock_movements,
    get_all_suppliers,
    get_movements_by_product,
    get_product_by_id,
    get_products_by_category,
    get_products_by_supplier,
    get_supplier_by_id,
    update_product_prices,
)
from reports import (
    get_current_stock_by_product,
    get_low_stock_products,
    get_movements_with_product,
    get_potential_profit,
    get_total_purchase_value,
    get_total_selling_value,
)


def print_menu():
    print("\n" + "=" * 40)
    print("      Inventory Manager CLI")
    print("=" * 40)
    print(" 1. Создать категорию")
    print(" 2. Показать все категории")
    print(" 3. Создать поставщика")
    print(" 4. Показать всех поставщиков")
    print(" 5. Деактивировать поставщика")
    print(" 6. Создать товар")
    print(" 7. Показать все товары")
    print(" 8. Показать товар по id")
    print(" 9. Обновить цену товара")
    print("10. Деактивировать товар")
    print("11. Добавить поступление товара")
    print("12. Добавить списание товара")
    print("13. Добавить корректировку остатка")
    print("14. Показать историю операций")
    print("15. Показать операции по товару")
    print("16. Показать текущие остатки")
    print("17. Показать товары, которые заканчиваются")
    print("18. Показать общую стоимость склада")
    print("19. Показать товары по категориям")
    print("20. Показать товары по поставщикам")
    print(" 0. Выход")
    print("=" * 40)


def main():
    Base.metadata.create_all(engine)

    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            name = input("Название категории: ").strip()
            category = create_category(name)
            if category:
                print(f"Категория '{category.name}' создана (id={category.id}).")

        elif choice == "2":
            categories = get_all_categories()
            if not categories:
                print("Нет категорий.")
            else:
                print(f"{'ID':<5} {'Название':<25}")
                print("-" * 30)
                for cat in categories:
                    print(f"{cat.id:<5} {cat.name:<25}")

        elif choice == "3":
            name = input("Название поставщика: ").strip()
            phone = input("Телефон (Enter пропустить): ").strip() or None
            email = input("Email (Enter пропустить): ").strip() or None
            supplier = create_supplier(name, phone, email)
            if supplier:
                print(
                    f"Поставщик '{supplier.name}' создан (id={supplier.id})."
                )

        elif choice == "4":
            suppliers = get_all_suppliers()
            if not suppliers:
                print("Нет поставщиков.")
            else:
                print(f"{'ID':<5} {'Название':<20} {'Активен':<10}")
                print("-" * 35)
                for s in suppliers:
                    active = "Да" if s.is_active else "Нет"
                    print(f"{s.id:<5} {s.name:<20} {active:<10}")

        elif choice == "5":
            try:
                supplier_id = int(input("ID поставщика: ").strip())
                deactivate_supplier(supplier_id)
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "6":
            name = input("Название товара: ").strip()
            sku = input("SKU: ").strip()

            raw = input("ID категории (Enter пропустить): ").strip()
            category_id = int(raw) if raw else None

            raw = input("ID поставщика (Enter пропустить): ").strip()
            supplier_id = int(raw) if raw else None

            raw = input("Закупочная цена (Enter пропустить): ").strip()
            purchase_price = Decimal(raw) if raw else None

            raw = input("Продажная цена (Enter пропустить): ").strip()
            selling_price = Decimal(raw) if raw else None

            raw = input("Минимальный остаток (Enter пропустить): ").strip()
            min_quantity = int(raw) if raw else None

            product = create_product(
                name,
                sku,
                category_id,
                supplier_id,
                purchase_price,
                selling_price,
                min_quantity,
            )
            if product:
                print(f"Товар '{product.name}' создан (id={product.id}).")

        elif choice == "7":
            products = get_all_products()
            if not products:
                print("Нет товаров.")
            else:
                print(f"{'ID':<5} {'Название':<30} {'SKU':<10} {'Активен':<10}")
                print("-" * 55)
                for p in products:
                    active = "Да" if p.is_active else "Нет"
                    print(f"{p.id:<5} {p.name:<30} {p.sku:<10} {active:<10}")

        elif choice == "8":
            try:
                product_id = int(input("ID товара: ").strip())
                p = get_product_by_id(product_id)
                if p:
                    print(f"ID: {p.id}")
                    print(f"Название: {p.name}")
                    print(f"SKU: {p.sku}")
                    print(f"ID категории: {p.category_id}")
                    print(f"ID поставщика: {p.supplier_id}")
                    print(f"Закупочная цена: {p.purchase_price}")
                    print(f"Продажная цена: {p.selling_price}")
                    print(f"Минимальный остаток: {p.min_quantity}")
                    print(f"Активен: {'Да' if p.is_active else 'Нет'}")
                    print(f"Дата создания: {p.created_at}")
                else:
                    print(f"Товар с id {product_id} не найден.")
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "9":
            try:
                product_id = int(input("ID товара: ").strip())

                raw = input(
                    "Новая закупочная цена (Enter не менять): "
                ).strip()
                purchase_price = Decimal(raw) if raw else None

                raw = input(
                    "Новая продажная цена (Enter не менять): "
                ).strip()
                selling_price = Decimal(raw) if raw else None

                product = update_product_prices(
                    product_id, purchase_price, selling_price
                )
                if product:
                    print(f"Цены товара '{product.name}' обновлены.")
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "10":
            try:
                product_id = int(input("ID товара: ").strip())
                deactivate_product(product_id)
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "11":
            try:
                product_id = int(input("ID товара: ").strip())
                quantity = int(input("Количество: ").strip())
                comment = input("Комментарий (Enter пропустить): ").strip() or None
                movement = create_stock_movement(
                    product_id, "IN", quantity, comment
                )
                if movement:
                    print("Поступление добавлено.")
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "12":
            try:
                product_id = int(input("ID товара: ").strip())
                quantity = int(input("Количество: ").strip())
                comment = input("Комментарий (Enter пропустить): ").strip() or None
                movement = create_stock_movement(
                    product_id, "OUT", quantity, comment
                )
                if movement:
                    print("Списание добавлено.")
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "13":
            try:
                product_id = int(input("ID товара: ").strip())
                quantity = int(input("Количество: ").strip())
                comment = input("Комментарий (Enter пропустить): ").strip() or None
                movement = create_stock_movement(
                    product_id, "ADJUST", quantity, comment
                )
                if movement:
                    print("Корректировка добавлена.")
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "14":
            rows = get_movements_with_product()
            if not rows:
                print("Нет операций.")
            else:
                h = f"{'Дата':<15} {'Товар':<25} {'SKU':<10} {'Тип':<8} {'Кол-во':<8} {'Комментарий':<20}"
                print(h)
                print("-" * len(h))
                for r in rows:
                    print(
                        f"{str(r.created_at):<15} {r.product_name:<25} {r.sku:<10} "
                        f"{r.movement_type:<8} {r.quantity:<8} {(r.comment or ''):<20}"
                    )

        elif choice == "15":
            try:
                product_id = int(input("ID товара: ").strip())
                movements = get_movements_by_product(product_id)
                if not movements:
                    print("Нет операций по этому товару.")
                else:
                    print(
                        f"{'ID':<5} {'Дата':<15} {'Тип':<8} {'Кол-во':<8} {'Комментарий':<20}"
                    )
                    print("-" * 56)
                    for m in movements:
                        print(
                            f"{m.id:<5} {str(m.created_at):<15} {m.movement_type:<8} "
                            f"{m.quantity:<8} {(m.comment or ''):<20}"
                        )
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == "16":
            rows = get_current_stock_by_product()
            if not rows:
                print("Нет товаров.")
            else:
                print(f"{'ID':<5} {'Товар':<30} {'Остаток':<10}")
                print("-" * 45)
                for row in rows:
                    print(f"{row.id:<5} {row.name:<30} {row.current_stock:<10}")

        elif choice == "17":
            rows = get_low_stock_products()
            if not rows:
                print("Нет товаров, которые заканчиваются.")
            else:
                print(
                    f"{'ID':<5} {'Товар':<30} {'Остаток':<10} {'Мин. остаток':<15}"
                )
                print("-" * 60)
                for row in rows:
                    print(
                        f"{row.id:<5} {row.name:<30} "
                        f"{row.current_stock:<10} {row.min_quantity:<15}"
                    )

        elif choice == "18":
            print()
            purchase_value = get_total_purchase_value()
            print(f"Закупочная стоимость склада: {purchase_value:.2f}")

            selling_value = get_total_selling_value()
            print(f"Потенциальная выручка:       {selling_value:.2f}")

            profit = get_potential_profit()
            print(f"Потенциальная прибыль:       {profit:.2f}")

        elif choice == "19":
            categories = get_all_categories()
            if not categories:
                print("Нет категорий.")
            else:
                print("Категории:")
                for cat in categories:
                    print(f"  {cat.id}. {cat.name}")

                try:
                    cat_id = int(input("\nВведите ID категории: ").strip())
                    products = get_products_by_category(cat_id)
                    if not products:
                        print("В этой категории нет товаров.")
                    else:
                        print(
                            f"\n{'ID':<5} {'Название':<30} {'SKU':<10}"
                        )
                        print("-" * 45)
                        for p in products:
                            print(f"{p.id:<5} {p.name:<30} {p.sku:<10}")
                except ValueError:
                    print("Ошибка: введите число.")

        elif choice == "20":
            suppliers = get_all_suppliers()
            if not suppliers:
                print("Нет поставщиков.")
            else:
                print("Поставщики:")
                for s in suppliers:
                    print(f"  {s.id}. {s.name}")

                try:
                    sup_id = int(input("\nВведите ID поставщика: ").strip())
                    products = get_products_by_supplier(sup_id)
                    if not products:
                        print("У этого поставщика нет товаров.")
                    else:
                        print(
                            f"\n{'ID':<5} {'Название':<30} {'SKU':<10}"
                        )
                        print("-" * 45)
                        for p in products:
                            print(f"{p.id:<5} {p.name:<30} {p.sku:<10}")
                except ValueError:
                    print("Ошибка: введите число.")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный пункт. Попробуйте снова.")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
