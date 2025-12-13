import javafx.beans.property.DoubleProperty;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class Film {
    // Properti Data Murni (sesuai kolom di CSV)
    private StringProperty title;
    private DoubleProperty voteAverage;
    private DoubleProperty popularity;
    private StringProperty releaseDate;
    private DoubleProperty voteCount; // Menggunakan DoubleProperty untuk kemudahan parsing awal

    public Film(String title, double voteAverage, double popularity, String releaseDate, double voteCount) {
        this.title = new SimpleStringProperty(title);
        this.voteAverage = new SimpleDoubleProperty(voteAverage);
        this.popularity = new SimpleDoubleProperty(popularity);
        this.releaseDate = new SimpleStringProperty(releaseDate);
        this.voteCount = new SimpleDoubleProperty(voteCount);
    }

    // --- GETTERS (Wajib untuk TableView) ---
    // TableView akan mencari metode dengan akhiran Property()
    public StringProperty titleProperty() {
        return title;
    }

    public DoubleProperty voteAverageProperty() {
        return voteAverage;
    }

    public DoubleProperty popularityProperty() {
        return popularity;
    }

    // Getter untuk sorting (digunakan di DataProcessor)
    public double getVoteAverage() {
        return voteAverage.get();
    }
}