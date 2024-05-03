# To change when we have the package and modules done
# from package.module import class
# from fftrack.audio.fft_processor import FFT_Processor

import logging
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

# Constants needed from audio, need to be imported too
DEFAULT_FS = 44100  # Sampling rate
DEFAULT_WINDOW_SIZE = 4096  # Size of the FFT window
DEFAULT_OVERLAP_RATIO = 0.5  # Overlap ratio for FFT

# Flags for plotting and logging
PLOT = True
LOG_INFO = True

# Constants for matching
CONFIDENCE_THRESHOLD = 0.5  # Confidence threshold for a match


class Matcher:
    """
    Matches the fingerprint of the query with the fingerprints of the database.
    """

    def __init__(self, database_manager):
        """
        Initialises the matcher with the database manager.
        """
        self.db_manager = database_manager

    def get_best_match(self, sample_hashes):
        """
        Matches the sample hashes with the database.

        Args:
            sample_hashes (list): List of hashes in the format [(hash, offset), ...].

        Returns:
            tuple: A tuple of the best matching song ID and its match details.
        """
        # Find matches between sample hashes and the database
        matches, matches_per_song = self.find_matches(sample_hashes, plot=PLOT)

        # Align the matches to find the most probable song match
        aligned_results = self.align_matches(matches)

        # Find the best match based on the highest count (confidence)
        best_match = self.find_best_match(aligned_results)

        return best_match
    def find_matches(self, sample_hashes,  plot=False):
        """
        Find matches between sample hashes and the database.

        Args:
            sample_hashes (list): List of hashes in the format [(hash, offset), ...].
            plot (bool): Whether to plot the distribution of offset differences.

        Returns:
            tuple: tuple of the match results and the number of unique hashes for each song.
        """
        logging.info(f"Matching {len(sample_hashes)} fingerprints with the database.") if LOG_INFO else None

        # Number of hash matches for each song (before aligning)
        matches_per_song = defaultdict(int)
        # List of all the possible matches
        possible_matches = []

        for hsh, sampled_offset in sample_hashes:
            # print(f"Sample hash: ({hsh}, {sampled_offset})")
            # extracting the list of (song_id, offset) for the current hash
            matches_curr_hash = self.db_manager.get_fingerprint_by_hash(hsh)
            # print(f"Matches from the database: \n {matches_curr_hash}")

            for sid, db_offset in matches_curr_hash:
                # print(f"Current hash match: ({sid}, {db_offset})")
                # Counting hash matches per song, without regards to offset
                matches_per_song[sid] += 1

                offset_difference = db_offset - sampled_offset
                # Logically should be positive, but there are anomalies when it is negative
                if offset_difference >= 0:
                    #matches.append((sid, offset_difference))
                    possible_matches.append((sid, offset_difference))
                # print(f"Possible matches: {possible_matches}")

        return possible_matches, matches_per_song


    def align_matches(self, matches):
        """
        Aligns the time difference of matches to find the most probable song match.

        Params:
            matches (list): List of matches in the format [(song_id, offset_difference), ...].

        Returns:
            dict: A dictionary of aligned match results for each song.
        """
        logging.info(f"Aligning {len(matches)} matches.") if LOG_INFO else None

        #print(f"Aligning {len(matches)} matches.")

        offset_by_song = defaultdict(list)

        # Group offset differences by song
        #print("Offsets by song:")
        for sid, offset_difference in matches:
            offset_by_song[sid].append(offset_difference)
            #print(f"SID: {sid}, offset_difference: {offset_difference}")

        # Analyze offset differences to find the best match
        aligned_results = {}
        # Sum of all the matches to calculate confidence
        sum_matches = 0
        for sid, offsets in offset_by_song.items():
            # Find the most common offset and its count (only if it is over the benchmark)
            # Testing benchmark: 4 matches for the same offset difference
            offset_counts = Counter({freq: count for freq, count in Counter(offsets).items() if count >= 0})
            #print(f"Count of offsets by song: {offset_counts}")
            if offset_counts:
                most_common_offset, count = offset_counts.most_common(1)[0]
                sum_matches += count

                aligned_results[sid] = {
                    "song_id": sid,
                    "offset": most_common_offset,
                    "count": count
                }

        # Adding the confidence to the results
        for sid, info in aligned_results.items():
            most_common_offset = info["offset"]
            count = info["count"]

            info["confidence"] = count/sum_matches
            confidence = info["confidence"]

            logging.info(f"Song ID: {sid}, "
                         f"Most Common Offset: {most_common_offset} ({self._offset_to_seconds(most_common_offset)}s, "
                         f"Matches: {count}, "
                         f"Confidence: {confidence:.2f}"
                         ) if LOG_INFO else None

        if PLOT:
            # Plot the distribution of offset differences for each song
            plt.figure(figsize=(15, 7))
            for sid, offsets in offset_by_song.items():
                plt.hist(offsets, bins=50, alpha=0.5, label=sid)
            plt.title('Distribution of Offset Differences')
            plt.xlabel('Offset Difference')
            plt.ylabel('Count')
            plt.legend()
            plt.show()

        return aligned_results


    def find_best_match(self, aligned_results):
        """
        Finds the best match from aligned results based on the highest count (confidence).

        :param aligned_results: A dictionary of aligned match results for each song.
        :return: A tuple of the best matching song ID and its match details.
        """
        best_match = max(aligned_results.items(), key=lambda x: x[1]["count"])

        return best_match


    def _offset_to_seconds(self, offset):
        hop_size = DEFAULT_WINDOW_SIZE * (1 - DEFAULT_OVERLAP_RATIO)
        frame_duration = hop_size / DEFAULT_FS
        offset_in_seconds = offset * frame_duration

        return offset_in_seconds


#if __name__ == "__main__":
#    main()


######
#
# to do (general)
## test with a bigger database (20-100)
### for different sample lenghts
#### deduct a benchmark to enter the offset count
##
## test with a lot bigger database (100+ songs, the more the preferable)
### test matching time
##
## find the reason to anomalies when offset_difference is negative ?
#
######