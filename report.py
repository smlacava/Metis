from fpdf import FPDF
from distances import *
import matplotlib.pyplot as plt
from pathlib import Path


class report():
    def _scores_histogram(self, scores, group_name="", distribution_name="", bins=None, view=True, save=True,
                          outPath=None):
        """
        The _scores_histogram method shows and/or saves (in .png format) the histogram related to a scores array (FOR
        INTERNAL USE ONLY).

        :param scores:            it is the 1D-array representing the scores
        :param group_name:        it is the name of the analyzed group ("" by default)
        :param distribution_name: it is the name of the analyzed distribution ("" by default)
        :param bins:              it is the number of bins which has to be used (None by default, if None it will be
                                  computed automatically)
        :param view:              it has to be True in order to show the histogram, False otherwise (True by default)
        :param save:              it has to be True in order to save the histogram as group_distribution_hist.png, where
                                  group is the value of group_name and distribution is the value of distribution_name
                                  (True by default)
        :param outPath:           it is the path (directory) in which the resulting image has to be saved (None by
                                  default)
        """
        plt.hist(scores, bins)
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        plt.title(str(group_name) + " group " + distribution_name + " scores distribution")
        if save is True:
            plt.savefig(self._fullname(outPath, group_name + "_" + distribution_name + "_hist.png"))
        if view is True:
            plt.show()


    def _rates_plot(self, FAR, FRR, thresholds, group_name="", view=True, save=True, outPath=None):
        """
        The _rates_plot method shows and/or saves (in .png format) the plot of the False Acceptance Rates (FARs) and the
        False Rejection Rates (FRRs) related to a set of common thresholds (FOR INTERNAL USE ONLY).

        :param FAR:        it is the 1D-array containing the FAR for each threshold
        :param FRR:        it is the 1D-array containing the FRR for each threshold
        :param thresholds: it is the 1D-array containing the threshold values
        :param group_name: it is the name of the analyzed group ("" by default)
        :param view:       it has to be True in order to show the histogram, False otherwise (True by default)
        :param save:       it has to be True in order to save the histogram as group_rates.png, where group is the value
                           of group_name (True by default)
        :param outPath:    it is the path (directory) in which the resulting image has to be saved (None by default)
        """
        FAR = np.squeeze(np.array(FAR))
        FRR = np.squeeze(np.array(FRR))
        plt.plot(thresholds, FAR)
        plt.plot(thresholds, FRR)
        plt.xticks(ticks=[0, 0.5, 1], labels=["0", "0.5", "1"])
        plt.xlim((0, 1))
        plt.legend(["FAR", "FRR"])
        plt.ylabel('Rate')
        plt.xlabel('Threshold')
        plt.title(str(group_name) + " group FAR and FRR")
        if save is True:
            plt.savefig(self._fullname(outPath, group_name + "_rates.png"))
        if view is True:
            plt.show()


    def _scores_boxplot(self, first_scores, second_scores, first_name="", second_name="", distribution_name="",
                        view=True, save=True, outPath=None):
        """
        The _scores_boxplot method shows and/or saves (in .png format) the boxplot related two scores vectors(FOR
        INTERNAL USE ONLY).

        :param first_scores:      it is the 1D-array representing the scores related to the first group
        :param first_scores:      it is the 1D-array representing the scores related to the second group
        :param first_name:        it is the name of the first analyzed group ("" by default)
        :param second_name:       it is the name of the second analyzed group ("" by default)
        :param distribution_name: it is the name of the analyzed distribution ("" by default)
        :param view:              it has to be True in order to show the histogram, False otherwise (True by default)
        :param save:              it has to be True in order to save the histogram as distribution_dist.png, where
                                  distribution is the value of distribution_name (True by default)
        :param outPath:           it is the path (directory) in which the resulting image has to be saved (None by
                                  default)
        """
        first = np.squeeze(first_scores)
        second = np.squeeze(second_scores)
        scores = [first, second]
        fig, ax = plt.subplots()
        ax.set_title(distribution_name + " scores distributions")
        ax.boxplot(scores)
        if not (first_name is "") and not (second_name is ""):
            plt.xticks([1, 2], [first_name, second_name])
        if save is True:
            plt.savefig(self._fullname(outPath, distribution_name + "_dist.png"))
        if view is True:
            plt.show()


    def _report(self, biometric_analysis, statistical_analysis, permutation_test, first_name, second_name, first_EER,
                second_EER, rates_results, pvalue, d, statistical_results, statistical_results_p, statistical_results2,
                statistical_results_d, pvalue_G, d_G, pvalue_I, d_I, p_perm, permutation_results,
                permutation_results_p, pdf_name, outPath, double_analysis):
        """
        The _report method is used to generate the pdf report of the analysis between two different groups (FOR INTERNAL
        USE ONLY).

        :param biometric_analysis:    it is True if the biometric analysis was computed, False otherwise
        :param statistical_analysis:  it is True if the statistical analysis was computed, False otherwise
        :param permutation_test:      it s True if the permutation_test was computed, False otherwise
        :param first_name:            it is the name of the first group
        :param second_name:           it is the name of the second group
        :param first_EER:             it is the Equality Error Rate related to the first group
        :param second_EER:            it is the Equality Error Rate related to the second group
        :param pvalue:                it is the pvalue 2D-matrix related to the comparison of the features between the
                                      two groups
        :param d:                     it is the Cohen's d 2D-matrix related to the comparison of the features between
                                      the two groups
        :param statistical_results:   it is a string representing a summary of the statistical results on the comparison
                                      between features of the different groups
        :param statistical_results_p: it is the string representing the pvalue table of the statistical results on the
                                      comparison between features of the different groups
        :param statistical_results2:  it is a string representing another summary of the statistical results on the
                                      comparison between features of the different groups
        :param statistical_results_d: it is the string representing the Cohen's d  table of the statistical results on
                                      the comparison  between features of the different groups
        :param pvalue_G:              it is the pvalue of the comparison between the genuine scores related to the
                                      different groups
        :param d_G:                   it is the Cohen's d value of the comparison between the genuine scores related to
                                      the two different groups
        :param pvalue_I:              it is the pvalue of the comparison between the impostor scores related to the two
                                      different groups
        :param d_I:                   it is the Cohen's d value of the comparison between the impostor scores related to
                                      the two different groups
        :param p_perm:                it is the pvalue 2D-matrix related to the permutation test on the features between
                                      the two groups
        :param permutation_results:   it is a string representing a summary of the permutation test results on the
                                      comparison between features of the different groups
        :param permutation_results_p: it is the string representing the pvalue table of the permutation test results on
                                      the comparison between features of the different groups
        :param pdf_name:              it is the name of the resulting report pdf
        :param outPath:               it is the path (directory) in which the resulting report has to be saved (None by
                                      default)
        :param double_analysis:       it has to be True if the computed analysis is on two different data matrices,
                                      False otherwise
        """
        print('Generating the report')
        pdf = FPDF()
        pdf_size = {'w': 210, 'h': 297}  # A4
        pdf.add_page()
        title = 24
        cap = 16
        text = 12
        cellh = 6
        tabh = 6
        pdf.set_font('Arial', 'B', title)
        leftx = pdf.get_x()
        pdf.multi_cell(0, 10, "Report", 0, 'C')
        pdf.set_font('Arial', 'B', cap)
        if biometric_analysis is True:
            pdf.multi_cell(0, cellh, "\n  EER results", 1)
        pdf.set_font('Arial', '', text)

        if double_analysis is True:
            tabw = int(max([pdf.get_string_width(first_name), pdf.get_string_width(second_name),
                            pdf.get_string_width("Cohen's d")]) * 1.5)
        else:
            tabw = int(max([pdf.get_string_width(first_name), pdf.get_string_width("-9.9999")])*1.5)

        y = pdf.get_y() + 5
        x = pdf.get_x()
        xstart = (pdf_size['w'] / 2) - tabw
        wimg = tabw * 5
        himg = int(wimg * 0.75)
        ximg = (pdf_size['w'] - wimg) / 2

        if biometric_analysis is True:
            if double_analysis is True:
                EER_title = "EERs"
            else:
                EER_title = "EER"

            pdf.set_xy(xstart, y)
            pdf.multi_cell(tabw * 2, tabh, EER_title, border=1, align='C', fill=0)
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_xy(xstart, y)
            pdf.multi_cell(tabw, tabh, first_name, border=1, align='L', fill=0)
            pdf.set_xy(xstart + tabw, y)
            pdf.multi_cell(tabw, tabh, str(round(first_EER, 5)), border=1, align='L', fill=0)

            if double_analysis is True:
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_xy(xstart, y)
                pdf.multi_cell(tabw, tabh, second_name, border=1, align='L', fill=0)
                pdf.set_xy(xstart + tabw, y)
                pdf.multi_cell(tabw, tabh, str(round(second_EER, 5)), border=1, align='L', fill=0)

            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)

            pdf.image(self._fullname(outPath, first_name) + "_Genuine_hist.png", ximg, None, wimg, himg)
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            if double_analysis is True:
                pdf.image(self._fullname(outPath, second_name) + "_Genuine_hist.png", ximg, None, wimg, himg)
                pdf.add_page()
                y = pdf.get_y()
                pdf.set_xy(leftx, y + 5)

            pdf.image(self._fullname(outPath, first_name) + "_Impostor_hist.png", ximg, None, wimg, himg)
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            if double_analysis is True:
                pdf.image(self._fullname(outPath, second_name) + "_Impostor_hist.png", ximg, None, wimg, himg)
                y = pdf.get_y()

            pdf.add_page()
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            pdf.set_font('Arial', 'B', cap)
            pdf.multi_cell(0, cellh, "\n FAR and FRR\n", 1)
            pdf.set_font('Arial', '', text)
            pdf.multi_cell(0, cellh, rates_results, 0)
            pdf.image(self._fullname(outPath, first_name) + "_rates.png", ximg, None, wimg, himg)
            if double_analysis is True:
                pdf.image(self._fullname(outPath, second_name) + "_rates.png", ximg, None, wimg, himg)
            pdf.add_page()

        if statistical_analysis is True or permutation_test is True:
            features_row = "            "
            if not(pvalue is None):
                repetitions = len(pvalue)
                features = len(pvalue[0])
            else:
                repetitions = len(p_perm)
                features = len(p_perm[0])
            for f in range(1, features + 1):
                features_row += "F"
                features_row += str(f)
                features_row += " " * (14 - len(str(f)))

        if permutation_test is True:
            y = pdf.get_y()
            pdf.set_xy(leftx, y)
            pdf.set_font('Arial', 'B', cap)
            pdf.multi_cell(0, cellh, "\n  Features permutation test results\n", 1)
            pdf.set_font('Arial', '', text)
            pdf.multi_cell(0, cellh, permutation_results + "\n", 0)
            pdf.multi_cell(0, cellh - 2, features_row, 0)
            pdf.multi_cell(0, cellh, permutation_results_p, 0)
            pdf.add_page()

        if statistical_analysis is True:
            y = pdf.get_y()
            pdf.set_xy(leftx, y)
            pdf.set_font('Arial', 'B', cap)
            pdf.multi_cell(0, cellh, "\n  Features statistical analysis results\n", 1)
            pdf.set_font('Arial', '', text)
            pdf.multi_cell(0, cellh, statistical_results + "\n", 0)
            pdf.multi_cell(0, cellh - 2, features_row, 0)
            pdf.multi_cell(0, cellh, statistical_results_p, 0)
            pdf.multi_cell(0, cellh, statistical_results2, 0)
            pdf.multi_cell(0, cellh - 2, features_row, 0)
            pdf.multi_cell(0, cellh, statistical_results_d, 0)
            pdf.add_page()

            if biometric_analysis is True:
                y = pdf.get_y()
                pdf.set_xy(leftx, y)
                pdf.set_font('Arial', 'B', cap)
                pdf.multi_cell(0, cellh, "\n  Genuine and Impostors statistical analysis results\n", 1)
                pdf.set_font('Arial', '', text)

                x = pdf.get_x()
                y = pdf.get_y() + 5
                xstart_2 = (pdf_size['w'] / 2) - int(1.5 * tabw)
                pdf.set_xy(xstart_2, y)
                pdf.multi_cell(tabw, tabh, "Scores", border=1, align='C', fill=0)
                pdf.set_xy(xstart_2 + tabw, y)
                pdf.multi_cell(tabw, tabh, "p-values", border=1, align='C', fill=0)
                pdf.set_xy(xstart_2 + 2 * tabw, y)
                pdf.multi_cell(tabw, tabh, "Cohen's d", border=1, align='C', fill=0)
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_xy(xstart_2, y)
                pdf.multi_cell(tabw, tabh, "Genuine", border=1, align='L', fill=0)
                pdf.set_xy(xstart_2 + tabw, y)
                pdf.multi_cell(tabw, tabh, str(round(pvalue_G, 5)), border=1, align='L', fill=0)
                pdf.set_xy(xstart_2 + 2 * tabw, y)
                pdf.multi_cell(tabw, tabh, str(round(d_G, 5)), border=1, align='L', fill=0)
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_xy(xstart_2, y)
                pdf.multi_cell(tabw, tabh, "Impostor", border=1, align='L', fill=0)
                pdf.set_xy(xstart_2 + tabw, y)
                pdf.multi_cell(tabw, tabh, str(round(pvalue_I, 5)), border=1, align='L', fill=0)
                pdf.set_xy(xstart_2 + 2 * tabw, y)
                pdf.multi_cell(tabw, tabh, str(round(d_I, 5)), border=1, align='L', fill=0)
                y = pdf.get_y()
                pdf.set_xy(leftx, y + 5)
                pdf.image(self._fullname(outPath, "Genuine_dist.png"), ximg, None, wimg, himg)
                pdf.image(self._fullname(outPath, "Impostor_dist.png"), ximg, None, wimg, himg)
        print('Report saved as ' + pdf_name)
        pdf.output(pdf_name, 'F')


    def _compute_thresholds(self, threshold):
        """
        The _compute_thresholds method computes the list of thresholds to use in generating the plots related to the
        FAR and the FRR (FOR INTERNAL USE ONLY).

        :param thresholds: it is a float number representing the step between two threshold values

        :return:           the list of thresholds
        """
        thr = threshold
        limit = int(1 / threshold)
        thresholds = [x * thr for x in range(limit)]
        thresholds.append(1)
        return thresholds


    def _fullname(self, parent, filename):
        """
        The _fullname method returns the full name of a file (FOR INTERNAL USE ONLY).

        :param parent:   it is the parent directory containing (or which will contain) the file
        :param filename: it is the name of the file

        :return: the fill name of the file
        """
        if not(parent is None):
            return str(Path(parent) / filename)
        else:
            return filename


    def single_analysis(self, data_manager, statan, biom, features_selector, perm_test,
                        data, labels=None, distance=euclidean_distance(), threshold=None,
                        view_analysis=False, generate_pdf=False,
                        name="first", bins=None, report_name="report.pdf", outPath=None,
                        selection_algorithm=None, selected_features=None, biometric_analysis=True):
        """
        The single_analysis method computes an analysis on a single data matrix, eventually reporting it on a pdf file.

        :param data_manager:        it is the object which manages the data
        :param statan:              it is the object which manages the statistical analysis
        :param biom:                it is the object which manages the biometric analysis
        :param features_selector:   it is the object which manages the feature selection
        :param perm_test:           it is the object which manages the permutation test
        :param data:                it is the first (subjects*repetitions*features) data matrix
        :param distance:            it is the function (or one string between 'euclidean', 'mahalanobis', 'manhattan'
                                    and 'minkowski', representing the homonymous distances) which is used in order to
                                    evaluate the distance in the genuine and impostor scores computation (optional,
                                    euclidean distance by default)
        :param threshold:           it is the step between two consecutive thresholds on which evaluate the FAR and the
                                    FRR, or None to automatically evaluate the threshold values (None by default)
        :param view_analysis:       it has to be True in order to print the results of the analysis, False otherwise
                                    (False by default)
        :param generate_pdf:        it has to be True in order to create the pdf of the analysis report, False otherwise
                                    (False by default)
        :param name:                it is the name of the first group ("first" by default)
        :param bins:                it is the number of bins which has to be used (None by default, if None it will be
                                    computed automatically)
        :param report_name:         it is the name of the eventually generated pdf ("report.pdf" by default)
        :param outPath:             it is the name of the directory in which export the report and the related figures
                                    (None by default)
        :param selection_algorithm: it is the selection algorithm, between None (all selected), 'ica', 'pca' and
                                    'columns' (None by default)
        :param selected_fetures:    it is the list of features (in caso of columns selection algorithm) or the number of
                                    features which have to be extracted (None by default)
        :param biometric_analysis:  it has to be True in order to execute the biometric analysis, False otherwise
                                    (True by default)
        """
        EER = None
        rates_results = None

        report_name = self._fullname(outPath, report_name)

        first_data, first_labels = data_manager.data_management(data, labels)
        if not (selection_algorithm is None or selected_features is None):
            data = features_selector.select_features(selection_algorithm, data,
                                                     selected_features)
        if biometric_analysis is True:
            scores = biom.compute_scores(data, distance)
            G, I, thr = biom.genuines_and_impostors(scores, labels)
            if not(threshold is None):
                thr = self._compute_thresholds(threshold)
            FAR, FRR, CRR, CAR, EER = biom.compute_performance_analysis(G, I, thr)

            if view_analysis is True or generate_pdf is True:
                EER_scores_results = "EER of the " + str(name) + " group: %.5f" % EER
                EER_scores_results += "\n\nGenuine and Impostor scores distributions:"
                rates_results = "\n\nFalse Acceptance Rates and False Rejection Rates:"

                if view_analysis is True:
                    print(EER_scores_results)
                self._scores_histogram(G, name, "Genuine", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(I, name, "Impostor", bins, view_analysis, generate_pdf, outPath)

                if view_analysis is True:
                    print(rates_results)
                self._rates_plot(FAR, FRR, thr, name, view_analysis, generate_pdf, outPath)

        if generate_pdf is True:
            if not (".pdf" in report_name):
                report_name += ".pdf"
            self._report(biometric_analysis, False, False, name, None, EER, None, rates_results, None, None, None, None, None,
                         None, None, None, None, None, None, None, None, report_name, outPath, double_analysis=False)


    def groups_comparison(self, data_manager, statan, biom, features_selector, perm_test, first_data, second_data=None,
                          first_labels=None, second_labels=None, distance=euclidean_distance(), threshold=None,
                          view_analysis=False, generate_pdf=False, first_name="first", second_name="second", bins=None,
                          report_name="report.pdf", outPath=None, selection_algorithm=None, selected_features=None,
                          permutation_test=False, permutation_method='approximate', permutation_assumption='different',
                          permutation_repetitions=100, biometric_analysis=True, statistical_analysis=True):
        """
        The groups_comparison method computes an analysis between two groups, represented as two different 3D
        (subjects*repetitions*features) data matrices, eventually reporting it on a pdf file.

        :param data_manager:            it is the object which manages the data
        :param statan:                  it is the object which manages the statistical analysis
        :param biom:                    it is the object which manages the biometric analysis
        :param features_selector:       it is the object which manages the feature selection
        :param perm_test:               it is the object which manages the permutation test
        :param first_data:              it is the first (subjects*repetitions*features) data matrix
        :param second_data:             it is the second (subjects*repetitions*features) data matrix (None by default, a
                                        previously inserted matrix will be used if it is None)
        :param distance:                it is the function (or one string between 'euclidean', 'mahalanobis',
                                        'manhattan' and 'minkowski', representing the homonymous distances) which is
                                        used in order to evaluate the distance in the genuine and impostor scores
                                        computation (optional, euclidean distance by default)
        :param threshold:               it is the step between two consecutive thresholds on which evaluate the FAR and
                                        the FRR, or None to automatically evaluate the threshold values (None by
                                        default)
        :param view_analysis:           it has to be True in order to print the results of the analysis, False otherwise
                                        (False by default)
        :param generate_pdf:            it has to be True in order to create the pdf of the analysis report, False
                                        otherwise (False by default)
        :param first_name:              it is the name of the first group ("first" by default)
        :param second_name:             it is the name of the second group ("second" by default)
        :param bins:                    it is the number of bins which has to be used (None by default, if None it will
                                        be computed automatically)
        :param report_name:             it is the name of the eventually generated pdf ("report.pdf" by default)
        :param outPath:                 it is the directory in which export the report and the related figures (None by
                                        default)
        :param selection_algorithm:     it is the selection algorithm, between None (all selected), 'ica', 'pca' and
                                        'columns' (None by default)
        :param selected_fetures:        it is the list of features (in caso of columns selection algorithm) or the number
                                        of features which have to be extracted (None by default)
        :param permutation_test:        it has to be True in order to execute the permutation test between the two
                                        datasets, False otherwise (False by default)
        :param permutation_method:      it is the pemutation test method, between 'approximate' and 'exact'
                                        ('approximate' by default)
        :param permutation_assumption:  it is the permutation test assumption, between 'different', 'higher' and
                                        'lower', representing the fact that the two means are different, the first is
                                        higher of the second one, or vice versa ('different' by default)
        :param permutation repetitions: it is the number of repetition of the approximate permutation test (100 by
                                        default, unused in the exact case)
        :param biometric_analysis:      it has to be True in order to execute the biometric analysis, False otherwise
                                        (True by default)
        :param statistical_analysis:    it has to be True in order to perform the statistical analysis, False otherwise
                                        (False by default)
        """
        pvalue, d, p_perm = None, None, None
        first_scores, first_G, first_I, first_thr = None, None, None, None
        second_scores, second_G, second_I, second_thr = None, None, None, None
        first_FAR, first_FRR, first_CRR, first_CAR, first_EER = None, None, None, None, None
        second_FAR, second_FRR, second_CRR, second_CAR, second_EER = None, None, None, None, None
        pvalue_G, d_G, pvalue_I, d_I = None, None, None, None
        rates_results = None

        report_name = self._fullname(outPath, report_name)

        first_data, first_labels = data_manager.data_management(first_data,
                                                                first_labels)
        second_data, second_labels = data_manager.data_management(second_data,
                                                                  second_labels)
        if not(selection_algorithm is None or selected_features is None):
            first_data = features_selector.select_features(selection_algorithm,
                                                           first_data,
                                                           selected_features)
            second_data = features_selector.select_features(selection_algorithm,
                                                            second_data,
                                                            selected_features)
        if permutation_test is True:
            print('Computing permutation test between features')
            p_perm = perm_test.compute_permutation_test(first_data, second_data, permutation_method,
                                                        permutation_assumption, permutation_repetitions, first_labels,
                                                        second_labels)

        if statistical_analysis is True:
            print('Computing statistical analysis between features')
            pvalue, d = statan.compute_features_statistics(first_data, second_data, first_labels, second_labels)

        if biometric_analysis is True:
            print('Computing genuine and impostor scores')
            first_scores = biom.compute_scores(first_data, distance)
            first_G, first_I, first_thr = biom.genuines_and_impostors(first_scores,
                                                                      first_labels)
            second_scores = biom.compute_scores(second_data, distance)
            second_G, second_I, second_thr = biom.genuines_and_impostors(second_scores,
                                                                     second_labels)
            if not(threshold is None):
                first_thr = self._compute_thresholds(threshold)
                second_thr = first_thr

            print('\nComputing biometric performance:\n First group:  ')
            first_FAR, first_FRR, first_CRR, first_CAR, first_EER = biom.compute_performance_analysis(first_G, first_I,
                                                                                                      first_thr)
            print("\n Second group: ")
            second_FAR, second_FRR, second_CRR, second_CAR, second_EER = biom.compute_performance_analysis(second_G,
                                                                                                           second_I,
                                                                                                           second_thr)
            print("")

            if statistical_analysis is True:
                print('\nComputing statistical analysis between scores')
                pvalue_G, d_G = statan.compute_scores_statistics(first_G, second_G)
                pvalue_I, d_I = statan.compute_scores_statistics(first_I, second_I)


        if view_analysis is True or generate_pdf is True:
            if biometric_analysis is True:
                EER_scores_results = "EER of the " + str(first_name) + " group: %.5f" % first_EER
                EER_scores_results += "\n\n"
                EER_scores_results += "EER of the " + str(second_name) + " group: %.5f" % second_EER
                EER_scores_results += "\n\nGenuine and Impostor scores distributions:"

                rates_results = "\n\nFalse Acceptance Rates and False Rejection Rates:"
                if statistical_analysis is True:
                    genuine_statistical_results = "\n\nResults of the statistical analysis between the two Genuine scores:\n\n  - pvalue:    %.5f" % pvalue_G
                    genuine_statistical_results += "\n  - Cohen's d: %.5f" % d_G
                    impostor_statistical_results = "\n\nResults of the statistical analysis between the two Impostor scores:\n\n  - pvalue:    %.5f" % pvalue_I
                    impostor_statistical_results += "\n  - Cohen's d: %.5f" % d_I


            statistical_results, features_row, statistical_results_p, statistical_results2, statistical_results_d = \
                self._statistical_strings(statistical_analysis, first_name, second_name, pvalue, d)
            permutation_results, features_row, permutation_results_p = self._permutation_strings(permutation_test,
                                                                                                 first_name,
                                                                                                 second_name,
                                                                                                 p_perm)

            if biometric_analysis is True:
                if view_analysis is True:
                    print(EER_scores_results)
                self._scores_histogram(first_G, first_name, "Genuine", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(second_G, second_name, "Genuine", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(first_I, first_name, "Impostor", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(second_I, second_name, "Impostor", bins, view_analysis, generate_pdf, outPath)

                if view_analysis is True:
                    print(rates_results)
                self._rates_plot(first_FAR, first_FRR, first_thr, first_name, view_analysis, generate_pdf, outPath)
                self._rates_plot(second_FAR, second_FRR, second_thr, second_name, view_analysis, generate_pdf, outPath)

            if permutation_test is True:
                print(permutation_results)
                print(features_row)
                print(permutation_results_p)

            if statistical_analysis is True:
                if view_analysis is True:
                    print(statistical_results)
                    print(features_row)
                    print(statistical_results_p)
                    print(statistical_results2)
                    print(features_row)
                    print(statistical_results_d)
                if biometric_analysis is True:
                    if view_analysis is True:
                        print(genuine_statistical_results)
                    self._scores_boxplot(first_G, second_G, first_name, second_name, "Genuine", view_analysis,
                                         generate_pdf, outPath)
                    if view_analysis is True:
                        print(impostor_statistical_results)
                    self._scores_boxplot(first_I, second_I, first_name, second_name, "Impostor", view_analysis,
                                         generate_pdf, outPath)

            if generate_pdf is True:
                if not (".pdf" in report_name):
                    report_name += ".pdf"
                self._report(biometric_analysis, statistical_analysis, permutation_test, first_name, second_name, first_EER, second_EER,
                             rates_results, pvalue, d, statistical_results,
                             statistical_results_p, statistical_results2,
                             statistical_results_d, pvalue_G, d_G, pvalue_I, d_I, p_perm, permutation_results,
                             permutation_results_p, report_name, outPath,
                             double_analysis=True)


    def _statistical_strings(self, statistical_analysis, first_name, second_name, pvalue, d):
        """
        The _statistical_strings method is used for generating the strings related to the statistical analysis results
        between features (FOR INTERNAL USE ONLY).

        :param statistical_analysis: True if statistical analysis were computed, False otherwise
        :param first_name:           the name of the first group of data
        :param second_name:          the name of the second group of data
        :param pvalue:               the matrix representing the p-value for each repetition (rows) and each feature
                                     (column)
        :param d:                    the matrix representing the Cohen's d for each repetition (rows) and each feature
                                     (column)

        :return:                     the strings related to the statistical results
        """
        statistical_results = ""
        features_row = ""
        statistical_results_p = ""
        statistical_results2 = ""
        statistical_results_d = ""
        if statistical_analysis is True:
            statistical_results = "\n\nResults of the statistical analysis on the features related to the "
            statistical_results += str(first_name) + " and the " + str(second_name) + " groups:\n\n  - P-value:\n"
            features_row = "        "
            repetitions = len(pvalue)
            features = len(pvalue[0])
            for f in range(1, features + 1):
                features_row += "F"
                features_row += str(f)
                features_row += " " * (10 - len(str(f)))

            statistical_results_p = "\n"
            for r in range(0, repetitions):
                statistical_results_p += "R"
                statistical_results_p += str(r + 1)
                for f in range(features):
                    statistical_results_p += "    %.5f" % pvalue[r, f]
                statistical_results_p += "\n"

            statistical_results2 = "\n\n  - Cohen's d:\n        "

            statistical_results_d = "\n"
            for r in range(0, repetitions):
                statistical_results_d += "R"
                statistical_results_d += str(r + 1)
                for f in range(features):
                    if d[r, f] < 0:
                        statistical_results_d += "   %.5f" % d[r, f]
                    else:
                        statistical_results_d += "    %.5f" % d[r, f]
                statistical_results_d += "\n"

        return statistical_results, features_row, statistical_results_p, statistical_results2, statistical_results_d


    def _permutation_strings(self, permutation_test, first_name, second_name, p_perm):
        """
        The _permutation_strings method is used for generating the strings related to the permutation test results
        between features (FOR INTERNAL USE ONLY).

        :param permutation_test: True if permutation test were computed, False otherwise
        :param first_name:       the name of the first group of data
        :param second_name:      the name of the second group of data
        :param p_perm:           it is the 2D matrix representing the p-value for each repetition (rows) and each
                                 feature (column)

        :return:                 the strings related to the permutation test results
        """
        permutation_results = ""
        features_row = ""
        permutation_results_p = ""
        if permutation_test is True:
            permutation_results = "\n\nResults of the statistical analysis on the features related to the "
            permutation_results += str(first_name) + " and the " + str(second_name) + " groups:\n\n  - P-value:\n"
            features_row = "        "
            repetitions = len(p_perm)
            features = len(p_perm[0])
            for f in range(1, features + 1):
                features_row += "F"
                features_row += str(f)
                features_row += " " * (10 - len(str(f)))

            permutation_results_p = "\n"
            for r in range(0, repetitions):
                permutation_results_p += "R"
                permutation_results_p += str(r + 1)
                for f in range(features):
                    permutation_results_p += "    %.5f" % p_perm[r, f]
                permutation_results_p += "\n"

        return permutation_results, features_row, permutation_results_p