from fpdf import FPDF
from distances import *
import matplotlib.pyplot as plt


class report():
    def _scores_histogram(self, scores, group_name="", distribution_name="", bins=None, view=True, save=True):
        """
        The _scores_histogram method shows and/or saves (in .png format) the
        histogram related to a scores array (FOR INTERNAL USE ONLY).

        :param scores:            it is the 1D-array representing the scores
        :param group_name:        it is the name of the analyzed group ("" by
                                  default)
        :param distribution_name: it is the name of the analyzed distribution ("" by
                                  default)
        :param bins:              it is the number of bins which has to be used
                                  (None by default, if None it will be computed
                                  automatically)
        :param view:              it has to be True in order to show the histogram,
                                  False otherwise (True by default)
        :param save:              it has to be True in order to save the histogram
                                  as group_distribution_hist.png, where group is the
                                  value of group_name and distribution is the value
                                  of distribution_name (True by default)
        """
        plt.hist(scores, bins)
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        plt.title(str(group_name) + " group " + distribution_name + " scores distribution")
        if save is True:
            plt.savefig(group_name + "_" + distribution_name + "_hist.png")
        if view is True:
            plt.show()

    def _rates_plot(self, FAR, FRR, thresholds, group_name="", view=True, save=True):
        """
        The _rates_plot method shows and/or saves (in .png format) the plot of the
        False Acceptance Rates (FARs) and the False Rejection Rates (FRRs) related
        to a set of common thresholds (FOR INTERNAL USE ONLY).

        :param FAR:        it is the 1D-array containing the FAR for each threshold
        :param FRR:        it is the 1D-array containing the FRR for each threshold
        :param thresholds: it is the 1D-array containing the threshold values
        :param group_name: it is the name of the analyzed group ("" by default)
        :param view:       it has to be True in order to show the histogram, False
                           otherwise (True by default)
        :param save:       it has to be True in order to save the histogram as
                           group_rates.png, where group is the value of group_name
                           (True by default)
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
            plt.savefig(group_name + "_rates.png")
        if view is True:
            plt.show()

    def _scores_boxplot(self, first_scores, second_scores, first_name="", second_name="", distribution_name="",
                        view=True, save=True):
        """
        The _scores_boxplot method shows and/or saves (in .png format) the boxplot
        related two scores vectors(FOR INTERNAL USE ONLY).

        :param first_scores:      it is the 1D-array representing the scores related
                                  to the first group
        :param first_scores:      it is the 1D-array representing the scores related
                                  to the second group
        :param first_name:        it is the name of the first analyzed group ("" by
                                  default)
        :param second_name:       it is the name of the second analyzed group ("" by
                                  default)
        :param distribution_name: it is the name of the analyzed distribution ("" by
                                  default)
        :param view:              it has to be True in order to show the histogram,
                                  False otherwise (True by default)
        :param save:              it has to be True in order to save the histogram
                                  as distribution_dist.png, where distribution is
                                  the value of distribution_name (True by default)
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
            plt.savefig(distribution_name + "_dist.png")
        if view is True:
            plt.show()

    def _report(self, first_name, second_name, first_EER, second_EER,
                rates_results, pvalue, d, statistical_results,
                statistical_results_p, statistical_results2,
                statistical_results_d, pvalue_G, d_G, pvalue_I, d_I, pdf_name,
                double_analysis):
        """
        The _report method is used to generate the pdf report of the analysis
        between two different groups (FOR INTERNAL USE ONLY).

        :param first_name:            it is the name of the first group
        :param second_name:           it is the name of the second group
        :param first_EER:             it is the Equality Error Rate related to the
                                      first group
        :param second_EER:            it is the Equality Error Rate related to the
                                      second group
        :param pvalue:                it is the pvalue 2D-matrix related to the
                                      comparison of the features between the two
                                      groups
        :param d:                     it is the Cohen's d 2D-matrix related to the
                                      comparison of the features between the two
                                      groups
        :param statistical_results:   it is a string representing a summary of the
                                      statistical results on the comparison between
                                      features of the different groups
        :param statistical_results_p: it is the string representing the pvalue table
                                      of the statistical results on the comparison
                                      between features of the different groups
        :param statistical_results2:  it is a string representing another summary of
                                      the statistical results on the comparison
                                      between features of the different groups
        :param statistical_results_d: it is the string representing the Cohen's d
                                      table of the statistical results on the
                                      comparison  between features of the different
                                      groups
        :param pvalue_G:              it is the pvalue of the comparison between the
                                      genuine scores related to the different groups
        :param d_G:                   it is the Cohen's d value of the comparison
                                      between the genuine scores related to the two
                                      different groups
        :param pvalue_I:              it is the pvalue of the comparison between the
                                      impostor scores related to the two different
                                      groups
        :param d_I:                   it is the Cohen's d value of the comparison
                                      between the impostor scores related to the two
                                      different groups
        """
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

        pdf.image(first_name + "_Genuine_hist.png", ximg, None, wimg, himg)
        y = pdf.get_y()
        pdf.set_xy(leftx, y + 5)
        if double_analysis is True:
            pdf.image(second_name + "_Genuine_hist.png", ximg, None, wimg, himg)
            pdf.add_page()
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)

        pdf.image(first_name + "_Impostor_hist.png", ximg, None, wimg, himg)
        y = pdf.get_y()
        pdf.set_xy(leftx, y + 5)
        if double_analysis is True:
            pdf.image(second_name + "_Impostor_hist.png", ximg, None, wimg, himg)
            y = pdf.get_y()

        pdf.add_page()
        y = pdf.get_y()
        pdf.set_xy(leftx, y + 5)
        pdf.set_font('Arial', 'B', cap)
        pdf.multi_cell(0, cellh, "\n FAR and FRR\n", 1)
        pdf.set_font('Arial', '', text)
        pdf.multi_cell(0, cellh, rates_results, 0)
        pdf.image(first_name + "_rates.png", ximg, None, wimg, himg)
        if double_analysis is True:
            pdf.image(second_name + "_rates.png", ximg, None, wimg, himg)

            features_row = "            "
            repetitions = len(pvalue)
            features = len(pvalue[0])
            for f in range(1, features + 1):
                features_row += "F"
                features_row += str(f)
                features_row += " " * (14 - len(str(f)))
            pdf.add_page()
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
            pdf.multi_cell(tabw, tabh, str(round(pvalue_G, 5)), border=1, align='L',
                           fill=0)
            pdf.set_xy(xstart_2 + 2 * tabw, y)
            pdf.multi_cell(tabw, tabh, str(round(d_G, 5)), border=1, align='L',
                           fill=0)
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_xy(xstart_2, y)
            pdf.multi_cell(tabw, tabh, "Impostor", border=1, align='L', fill=0)
            pdf.set_xy(xstart_2 + tabw, y)
            pdf.multi_cell(tabw, tabh, str(round(pvalue_I, 5)), border=1, align='L',
                           fill=0)
            pdf.set_xy(xstart_2 + 2 * tabw, y)
            pdf.multi_cell(tabw, tabh, str(round(d_I, 5)), border=1, align='L',
                           fill=0)
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            pdf.image("Genuine_dist.png", ximg, None, wimg, himg)
            pdf.image("Impostor_dist.png", ximg, None, wimg, himg)
        pdf.output(pdf_name, 'F')

    def single_analysis(self, data_manager, statan, biom, features_selector,
                        data, labels=None, distance=euclidean_distance(),
                        view_analysis=False, generate_pdf=False,
                        name="first", bins=None, report_name="report.pdf",
                        selection_algorithm=None, selected_features=None):
        first_data, first_labels = data_manager.data_management(data, labels)
        if not (selection_algorithm is None or selected_features is None):
            data = features_selector.select_features(selection_algorithm, data,
                                                     selected_features)
        scores = biom.compute_scores(data, distance)
        G, I, thr = biom.genuines_and_impostors(scores, labels)
        FAR, FRR, CRR, CAR, EER = biom.compute_performance_analysis(G, I, thr)

        if view_analysis is True or generate_pdf is True:
            EER_scores_results = "EER of the " + str(name) + " group: %.5f" % EER
            EER_scores_results += "\n\nGenuine and Impostor scores distributions:"
            rates_results = "\n\nFalse Acceptance Rates and False Rejection Rates:"

            if view_analysis is True:
                print(EER_scores_results)
            self._scores_histogram(G, name, "Genuine", bins, view_analysis, generate_pdf)
            self._scores_histogram(I, name, "Impostor", bins, view_analysis, generate_pdf)

            if view_analysis is True:
                print(rates_results)
            self._rates_plot(FAR, FRR, thr, name, view_analysis, generate_pdf)
            if generate_pdf is True:
                if not (".pdf" in report_name):
                    report_name += ".pdf"
                self._report(name, None, EER, None, rates_results, None,
                             None, None, None, None, None, None, None, None,
                             None, report_name, double_analysis=False)

    def groups_comparison(self, data_manager, statan, biom, features_selector,
                          first_data, second_data=None, first_labels=None,
                          second_labels=None, distance=euclidean_distance(),
                          view_analysis=False, generate_pdf=False,
                          first_name="first", second_name="second", bins=None,
                          report_name="report.pdf",
                          selection_algorithm=None, selected_features=None):
        """
        The groups_comparison method computes an analysis between two groups,
        represented as two different 3D (subjects*repetitions*features) data
        matrices, eventually reporting it on a pdf file.

        :param first_data:    it is the first (subjects*repetitions*features) data
                              matrix
        :param second_data:   it is the second (subjects*repetitions*features) data
                              matrix (None by default, a previously inserted matrix
                              will be used if it is None)
        :param distance:      it is the function (or one string between 'euclidean',
                              'manhattan' and 'minkowski', representing the
                              homonymous distances) which is used in order to
                              evaluate the distance in the genuine and impostor
                              scores computation (optional, euclidean distance by
                              default)
        :param view_analysis: it has to be True in order to print the results of the
                              analysis, False otherwise (False by default)
        :param generate_pdf:  it has to be True in order to create the pdf of the
                              analysis report, False otherwise (False by default)
        :param first_name:    it is the name of the first group ("first" by default)
        :param second_name:   it is the name of the second group ("second" by
                              default)
        :param bins:          it is the number of bins which has to be used (None by
                              default, if None it will be computed automatically)
        :params report_name:  it is the name of the eventually generated pdf
                              ("report.pdf" by default)
        """
        first_data, first_labels = data_manager.data_management(first_data,
                                                                first_labels)
        second_data, second_labels = data_manager.data_management(second_data,
                                                                  second_labels)
        pvalue, d = statan.compute_features_statistics(first_data, second_data,
                                                       first_labels, second_labels)
        if not(selection_algorithm is None or selected_features is None):
            first_data = features_selector.select_features(selection_algorithm,
                                                           first_data,
                                                           selected_features)
            second_data = features_selector.select_features(selection_algorithm,
                                                            second_data,
                                                            selected_features)
        first_scores = biom.compute_scores(first_data, distance)
        first_G, first_I, first_thr = biom.genuines_and_impostors(first_scores,
                                                                  first_labels)

        second_scores = biom.compute_scores(second_data, distance)
        second_G, second_I, second_thr = biom.genuines_and_impostors(second_scores,
                                                                     second_labels)

        first_FAR, first_FRR, first_CRR, first_CAR, first_EER = biom.compute_performance_analysis(first_G, first_I,
                                                                                                  first_thr)
        second_FAR, second_FRR, second_CRR, second_CAR, second_EER = biom.compute_performance_analysis(second_G,
                                                                                                       second_I,
                                                                                                       second_thr)
        pvalue_G, d_G = statan.compute_scores_statistics(first_G, second_G)
        pvalue_I, d_I = statan.compute_scores_statistics(first_I, second_I)

        if view_analysis is True or generate_pdf is True:
            EER_scores_results = "EER of the " + str(first_name) + " group: %.5f" % first_EER
            EER_scores_results += "\n\n"
            EER_scores_results += "EER of the " + str(second_name) + " group: %.5f" % second_EER
            EER_scores_results += "\n\nGenuine and Impostor scores distributions:"

            rates_results = "\n\nFalse Acceptance Rates and False Rejection Rates:"
            genuine_statistical_results = "\n\nResults of the statistical analysis between the two Genuine scores:\n\n  - pvalue:    %.5f" % pvalue_G
            genuine_statistical_results += "\n  - Cohen's d: %.5f" % d_G
            impostor_statistical_results = "\n\nResults of the statistical analysis between the two Impostor scores:\n\n  - pvalue:    %.5f" % pvalue_I
            impostor_statistical_results += "\n  - Cohen's d: %.5f" % d_I

            statistical_results = "\n\nResults of the statistical analysis on the features related to the " + str(
                first_name) + " and the " + str(second_name) + " groups:\n\n  - P-value:\n"
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

            if view_analysis is True:
                print(EER_scores_results)
            self._scores_histogram(first_G, first_name, "Genuine", bins, view_analysis, generate_pdf)
            self._scores_histogram(second_G, second_name, "Genuine", bins, view_analysis, generate_pdf)
            self._scores_histogram(first_I, first_name, "Impostor", bins, view_analysis, generate_pdf)
            self._scores_histogram(second_I, second_name, "Impostor", bins, view_analysis, generate_pdf)

            if view_analysis is True:
                print(rates_results)
            self._rates_plot(first_FAR, first_FRR, first_thr, first_name, view_analysis, generate_pdf)
            self._rates_plot(second_FAR, second_FRR, second_thr, second_name, view_analysis, generate_pdf)

            if view_analysis is True:
                print(statistical_results)
                print(features_row)
                print(statistical_results_p)
                print(statistical_results2)
                print(features_row)
                print(statistical_results_d)

            if view_analysis is True:
                print(genuine_statistical_results)
            self._scores_boxplot(first_G, second_G, first_name, second_name, "Genuine", view_analysis, generate_pdf)
            if view_analysis is True:
                print(impostor_statistical_results)
            self._scores_boxplot(first_I, second_I, first_name, second_name, "Impostor", view_analysis, generate_pdf)

            if generate_pdf is True:
                if not (".pdf" in report_name):
                    report_name += ".pdf"
                self._report(first_name, second_name, first_EER, second_EER,
                             rates_results, pvalue, d, statistical_results,
                             statistical_results_p, statistical_results2,
                             statistical_results_d, pvalue_G, d_G, pvalue_I, d_I, report_name,
                             double_analysis=True)

