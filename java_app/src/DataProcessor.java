

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class DataProcessor {

    public static ObservableList<Film> loadAndProcessData() {
        // PERHATIKAN PATH INI! HARUS MENUNJUK KE CSV RAW
        String csvFile = "./data/raw/Top_Rated_Movies.csv";

        List<Film> rawList = new java.util.ArrayList<>();
        String line = "";

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            br.readLine(); // Lewati header (baris pertama: ,id,title,...)
            while ((line = br.readLine()) != null) {
                // Split berdasarkan koma, tapi abaikan koma di dalam tanda kutip (")
                // PERHATIAN: Line dimulai dari 0,278,The Shawshank...
                String[] data = line.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");

                // Cek minimal harus ada 6 kolom yang kita pakai (mulai dari 0 sampai 5)
                if (data.length >= 6) {
                    try {
                        // KOREKSI INDEX SESUAI DATA SAMPLE KAMU:
                        String title = data[2].replace("\"", "").trim(); // Index 2 (Kolom ke-3)
                        double voteAverage = Double.parseDouble(data[3].trim()); // Index 3
                        double voteCount = Double.parseDouble(data[4].trim()); // Index 4
                        String releaseDate = data[5].replace("\"", "").trim(); // Index 5
                        double popularity = Double.parseDouble(data[6].trim()); // Index 6

                        rawList.add(new Film(title, voteAverage, popularity, releaseDate, voteCount));
                    } catch (NumberFormatException e) {
                        // System.err.println("Skip baris karena data angka rusak: " + line);
                        continue; // Lewati baris yang datanya tidak bisa diubah ke angka
                    } catch (ArrayIndexOutOfBoundsException e) {
                        // Terkadang ada baris terakhir yang kosong, kita abaikan
                        continue;
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("Gagal membaca file CSV. Cek path Working Directory atau keberadaan file.");
            e.printStackTrace();
            return FXCollections.emptyObservableList();
        }

        // --- FILTER DAN AMBIL 100 TERBAIK (Berdasarkan Rating) ---
        List<Film> top100List = rawList.stream()
                .sorted(Comparator.comparing(Film::getVoteAverage).reversed())
                .limit(100)
                .collect(Collectors.toList());

        return FXCollections.observableArrayList(top100List);
    }
}