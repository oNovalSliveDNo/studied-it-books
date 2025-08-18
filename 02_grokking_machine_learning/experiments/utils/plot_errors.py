import matplotlib.pyplot as plt


def plot_errors(errors_list, error_name: str, *,
                style: str = "line",  # "line" или "scatter"
                ax=None):
    """
    Строит график ошибок по эпохам обучения.

    Parameters:
        errors_list (list): Список значений ошибки (например, RMSE на каждой эпохе).
        error_name (str): Название ошибки (для отображения в заголовке).
        style (str): Тип графика: "line" (по умолчанию) или "scatter".
        ax (matplotlib.axes.Axes): Ось для отрисовки (если None — используется текущая).
    """
    if ax is None:
        ax = plt.gca()

    if style == "scatter":
        ax.scatter(range(len(errors_list)), errors_list, s=8, color="blue")

    else:  # по умолчанию "line"
        ax.plot(errors_list, "b-", linewidth=2)

    ax.set_title(f"{error_name.upper()} по эпохам")
    ax.set_xlabel("Эпоха")
    ax.set_ylabel(error_name.upper())
    ax.grid(True)

    return ax
