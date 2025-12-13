

import javafx.application.Application;
import javafx.collections.ObservableList;
import javafx.scene.Scene;
import javafx.scene.chart.BarChart;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Label;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        // 1. Ambil data yang sudah diproses
        ObservableList<Film> data = DataProcessor.loadAndProcessData();

        // 2. Buat Tampilan Utama (TabPane)
        TabPane tabPane = new TabPane();

        // --- TABEL (TAB 1) ---
        Tab tableTab = new Tab("Tabel Top 100 Film");
        tableTab.setContent(createTableView(data));
        tableTab.setClosable(false);

        // --- GRAFIK (TAB 2) ---
        Tab chartTab = new Tab("Grafik 10 Film Teratas");
        chartTab.setContent(createChartView(data));
        chartTab.setClosable(false);

        tabPane.getTabs().addAll(tableTab, chartTab);

        // 3. Setup Stage
        Scene scene = new Scene(tabPane, 800, 600);
        primaryStage.setTitle("Data Film Top 100 (JavaFX)");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    // --- FUNGSI MEMBUAT TABEL ---
    private VBox createTableView(ObservableList<Film> data) {
        TableView<Film> tableView = new TableView<>();

        // Kolom 1: Judul
        TableColumn<Film, String> titleCol = new TableColumn<>("Judul Film");
        titleCol.setCellValueFactory(cellData -> cellData.getValue().titleProperty());
        titleCol.setPrefWidth(350);

        // Kolom 2: Rating
        TableColumn<Film, Number> ratingCol = new TableColumn<>("Rating");
        ratingCol.setCellValueFactory(cellData -> cellData.getValue().voteAverageProperty());
        ratingCol.setPrefWidth(100);

        // Kolom 3: Popularitas
        TableColumn<Film, Number> popularityCol = new TableColumn<>("Popularitas");
        popularityCol.setCellValueFactory(cellData -> cellData.getValue().popularityProperty());
        popularityCol.setPrefWidth(150);

        // Tambahkan kolom ke TableView
        tableView.getColumns().addAll(titleCol, ratingCol, popularityCol);

        // Masukkan data
        tableView.setItems(data);

        return new VBox(new Label("100 Film Rating Tertinggi"), tableView);
    }

    // --- FUNGSI MEMBUAT GRAFIK ---
    private VBox createChartView(ObservableList<Film> data) {
        final CategoryAxis xAxis = new CategoryAxis();
        final NumberAxis yAxis = new NumberAxis();
        final BarChart<String, Number> barChart = new BarChart<>(xAxis, yAxis);

        barChart.setTitle("Popularitas 10 Film Teratas");
        xAxis.setLabel("Judul Film");
        yAxis.setLabel("Popularitas Score");
        barChart.setLegendVisible(false); // Hilangkan legenda karena cuma 1 seri

        XYChart.Series<String, Number> series = new XYChart.Series<>();

        // Ambil 10 teratas dari data yang sudah disortir (pastikan ada)
        for (int i = 0; i < Math.min(10, data.size()); i++) {
            Film film = data.get(i);
            // Hanya ambil 25 karakter judul agar tidak terlalu panjang di grafik
            String shortTitle = film.titleProperty().get().substring(0, Math.min(25, film.titleProperty().get().length()));
            series.getData().add(new XYChart.Data<>(shortTitle + "...", film.popularityProperty().get()));
        }

        barChart.getData().add(series);

        return new VBox(barChart);
    }

    public static void main(String[] args) {
        launch(args);
    }
}