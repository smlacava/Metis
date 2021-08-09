from fpdf import FPDF
from distances import *
import matplotlib.pyplot as plt
from pathlib import Path


class report():
    """
    The report class provides the methods which generates the analysis reports, in form of pdf documents and png images,
    as well as the analysis themselves.

    Methods:
        single_analysis:   computes the biometric analysis on the raw dataset
        groups_comparison: computes the biometric analysis on two raw datasets, and compares them through various
                           statistical analysis
        cluster_analysis:  computes the clustering on a raw dataset, and evaluates the performance of the results
    """


    def _roc_curve(self, FAR, CAR, group_name, view=True, save=True, outPath=None):
        """
        The _roc_curve method shows and/or saves (in .png format) the Receiver Operating Characteristic curve related to
        the system performance in terms of False Acceptance Rate and Correct Acceptance Rate (FOR INTERNAL USE ONLY).

        :param FAR:        it is the 1D-array representing the False Acceptance Rate for different thresholds
        :param CAR:        it is the 1D-array representing the Correct Acceptance Rate for different thresholds
        :param group_name: it is the name of the analyzed group ("" by default)
        :param view:       it has to be True in order to show the histogram, False otherwise (True by default)
        :param save:       it has to be True in order to save the histogram as group_droc.png, where group is the value
                           of group_name (True by default)
        :param outPath:    it is the path (directory) in which the resulting image has to be saved (None by default)
        """
        plt.plot(FAR, CAR)
        plt.xlabel("False Acceptance Rate")
        plt.ylabel("Correct Acceptance Rate")
        plt.title("ROC curve of the " + str(group_name) + " group")
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        if save is True:
            plt.savefig(self._fullname(outPath, group_name + "_roc.png"))
        if view is True:
            plt.show()

    def _roc_curve_comparison(self, first_FAR, first_CAR, second_FAR, second_CAR, first_name="first",
                              second_name="second", view=True, save=True, outPath=None):
        """
        The _roc_curve_comparison method shows in the same graph and/or saves (in .png format) the Receiver Operating
        Characteristic curves related to the system performance of two groups, in terms of False Acceptance Rate and
        Correct Acceptance Rate (FOR INTERNAL USE ONLY).

        :param first_FAR:   it is the 1D-array representing the False Acceptance Rate related to the first analyzed
                            group for different thresholds
        :param first_CAR:   it is the 1D-array representing the Correct Acceptance Rate related to the first analyzed
                            group for different thresholds
        :param second_FAR:  it is the 1D-array representing the False Acceptance Rate related to the second analyzed
                            group for different thresholds
        :param second_CAR:  it is the 1D-array representing the Correct Acceptance Rate related to the second analyzed
                            group for different thresholds
        :param first_name:  it is the name of the first analyzed group ("first" by default)
        :param second_name: it is the name of the second analyzed group ("second" by default)
        :param view:        it has to be True in order to show the histogram, False otherwise (True by default)
        :param save:        it has to be True in order to save the histogram as group_droc.png, where group is the value
                            of group_name (True by default)
        :param outPath:     it is the path (directory) in which the resulting image has to be saved (None by default)
        """
        plt.plot(first_FAR, first_CAR, label=first_name)
        plt.plot(second_FAR, second_CAR, label=second_name)
        plt.xlabel("False Acceptance Rate")
        plt.ylabel("Correct Acceptance Rate")
        plt.title("Comparison between ROC curves")
        plt.legend(loc='lower right')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        if save is True:
            plt.savefig(self._fullname(outPath, first_name + "_" + second_name + "_roc.png"))
        if view is True:
            plt.show()


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
        plt.xlim([0, 1])
        if save is True:
            plt.savefig(self._fullname(outPath, group_name + "_" + distribution_name + "_hist.png"))
        if view is True:
            plt.show()


    def _scores_histogram_comparison(self, first_scores, second_scores, group_name="", first_distribution_name="first",
                                     second_distribution_name="second", bins=None, view=True, save=True, outPath=None):
        """
        The _scores_histogram_comparison method shows and/or saves (in .png format) two compared histograms related to
        the same number of scores arrays (FOR INTERNAL USE ONLY).

        :param first_scores:              it is the 1D-array representing the first scores distribution
        :param second_scores:             it is the 1D-array representing the second scores distribution
        :param group_name:                it is the name of the first analyzed group ("" by default)
        :param first_distribution_name:   it is the name of the second analyzed group ("first" by default)
        :param seccond_distribution_name: it is the name of the analyzed distribution ("second" by default)
        :param bins:                      it is the number of bins which has to be used (None by default, if None it
                                          will be computed automatically)
        :param view:                      it has to be True in order to show the histogram, False otherwise (True by
                                          default)
        :param save:                      it has to be True in order to save the histogram as
                                          group_firstDistribution_secondDistribution_hist.png, where group is the value
                                          of group_name, firstDistribution is the value of first_distribution_name and
                                          secondDistribution is the value of second_distribution_name (True by default)
        :param outPath:                   it is the path (directory) in which the resulting image has to be saved (None
                                          by default)
        """

        plt.hist(first_scores, bins, label=first_distribution_name, histtype='step', density=True)
        plt.hist(second_scores, bins, label=second_distribution_name, histtype='step', density=True)
        plt.legend(loc='upper right')
        plt.xlabel('Score')
        plt.ylabel('Frequency [%]')
        plt.title(str(group_name) + "-" + first_distribution_name + " " + second_distribution_name +
                  " scores distribution")
        plt.xlim([0, 1])
        if save is True:
            plt.savefig(self._fullname(outPath, group_name + "_" + first_distribution_name + "_" +
                                       second_distribution_name + "_hist.png"))
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

    def _report_scores_descriptive_statistics(self, pdf, desc_stats, group_name, xstart_double, y, tabw, tabh):
        """
        The _report_scores_descriptive_statistics method generates a table related to descriptive statistics of genuine
        and impostor similarity scores distributions (FOR INTERNAL USE ONLY).

        :param pdf:           it is the handle to the report file
        :param desc_stats:    it is the dictionary related to the computed statistics
        :param group_name:    it is the name of the represented group
        :param xstart_double: it is the space between left margin and the beginning of the table
        :param y:             it is the current distance from the top margin
        :param tabw:          it is the width of each cell of the table
        :param tabh:          it is the height of each cell of the table

        :return:              the handle of the modified report
        """
        pdf.set_xy(xstart_double + tabw, y + 5)
        pdf.multi_cell(tabw * 2, tabh, group_name, border=1, align='C', fill=0)
        y = pdf.get_y()
        pdf.set_xy(xstart_double + tabw, y)
        pdf.multi_cell(tabw, tabh, "Genuines", border=1, align='C', fill=0)
        pdf.set_xy(xstart_double + (tabw * 2), y)
        pdf.multi_cell(tabw, tabh, "Impostors", border=1, align='C', fill=0)
        y = pdf.get_y()
        pdf.set_xy(xstart_double, y)
        pdf.multi_cell(tabw, tabh, "Mean", border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(desc_stats['mean'][0], 5)), border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + 2 * tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(desc_stats['mean'][1], 5)), border=1, align='L', fill=0)
        y = pdf.get_y()
        pdf.set_xy(xstart_double, y)
        pdf.multi_cell(tabw, tabh, "Median", border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(desc_stats['median'][0], 5)), border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + 2 * tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(desc_stats['median'][1], 5)), border=1, align='L', fill=0)
        y = pdf.get_y()
        pdf.set_xy(xstart_double, y)
        pdf.multi_cell(tabw, tabh, "Std", border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(desc_stats['std'][0], 5)), border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + 2 * tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(desc_stats['std'][1], 5)), border=1, align='L', fill=0)
        return pdf


    def _report_statistical_analysis(self, pdf, pvalues, ds, xstart_double, y, tabw, tabh):
        """
        The _report_statistical_analysis method generates a table related to p-values and the Cohen's d between the
        features related to the two groups (FOR INTERNAL USE ONLY).

        :param pdf:           it is the handle to the report file
        :param pvalues:       it is the array containing the pvalue related to each feature
        :param ds:            it is the array containting the Cohen's d related to each feature
        :param xstart_double: it is the space between left margin and the beginning of the table
        :param y:             it is the current distance from the top margin
        :param tabw:          it is the width of each cell of the table
        :param tabh:          it is the height of each cell of the table

        :return:              the handle of the modified report
        """

        pdf.set_xy(xstart_double + tabw, y+5)
        pdf.multi_cell(tabw, tabh, "p-value", border=1, align='C', fill=0)
        pdf.set_xy(xstart_double + (tabw * 2), y+5)
        pdf.multi_cell(tabw, tabh, "Cohen's d", border=1, align='C', fill=0)
        L = max(np.shape(pvalues))
        for i in range(L):
            y = pdf.get_y()
            pdf.set_xy(xstart_double, y)
            pdf.multi_cell(tabw, tabh, "F"+str(i+1), border=1, align='L', fill=0)
            pdf.set_xy(xstart_double + tabw, y)
            pdf.multi_cell(tabw, tabh, str(round(pvalues[i], 5)), border=1, align='L', fill=0)
            pdf.set_xy(xstart_double + 2 * tabw, y)
            pdf.multi_cell(tabw, tabh, str(round(ds[i], 5)), border=1, align='L', fill=0)
            if (i+1)%35 == 0 and i > 0:
                pdf.add_page()
        return pdf

    def _report_confusion_matrix(self, pdf, cm, group_name, xstart_double, y, tabw, tabh):
        """
        The _report_confusion_matrix method generates a table related to a confusion_matrix (FOR INTERNAL USE ONLY).

        :param pdf:           it is the handle to the report file
        :param cm:            it is the confusion matrix
        :param group_name:    it is the name of the represented group
        :param xstart_double: it is the space between left margin and the beginning of the table
        :param y:             it is the current distance from the top margin
        :param tabw:          it is the width of each cell of the table
        :param tabh:          it is the height of each cell of the table

        :return:              the handle of the modified report
        """
        pdf.set_xy(xstart_double + tabw, y + 5)
        pdf.multi_cell(tabw * 2, tabh, group_name, border=1, align='C', fill=0)
        y = pdf.get_y()
        pdf.set_xy(xstart_double + tabw, y)
        pdf.multi_cell(tabw, tabh, "Predicted G", border=1, align='C', fill=0)
        pdf.set_xy(xstart_double + (tabw * 2), y)
        pdf.multi_cell(tabw, tabh, "Predicted I", border=1, align='C', fill=0)
        y = pdf.get_y()
        pdf.set_xy(xstart_double, y)
        pdf.multi_cell(tabw, tabh, "True G", border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(cm[0][0], 5)), border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + 2 * tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(cm[0][1], 5)), border=1, align='L', fill=0)
        y = pdf.get_y()
        pdf.set_xy(xstart_double, y)
        pdf.multi_cell(tabw, tabh, "True I", border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(cm[1][0], 5)), border=1, align='L', fill=0)
        pdf.set_xy(xstart_double + 2 * tabw, y)
        pdf.multi_cell(tabw, tabh, str(round(cm[1][1], 5)), border=1, align='L', fill=0)
        return pdf


    def _report(self, biometric_analysis, statistical_analysis, permutation_test, first_name, second_name, first_EER,
                second_EER, first_AUC, second_AUC, first_desc_stats, second_desc_stats, first_cm, second_cm,
                rates_results, pvalues, ds, pvalue_G, d_G, pvalue_I, d_I, p_perm, permutation_results,
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
        :param pvalues:               it is the pvalue 2D-matrix related to the comparison of the features between the
                                      two groups
        :param ds:                    it is the Cohen's d 2D-matrix related to the comparison of the features between
                                      the two groups
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
            tabw = int(max([pdf.get_string_width(first_name), pdf.get_string_width("Cohen's d")]) * 1.5)

        y = pdf.get_y() + 5
        x = pdf.get_x()
        xstart = (pdf_size['w'] / 2) - tabw
        xstart_double = (pdf_size['w'] / 2) - (1.5*tabw)
        wimg = tabw * 5
        himg = int(wimg * 0.75)
        ximg = (pdf_size['w'] - wimg) / 2

        if biometric_analysis is True:
            if double_analysis is True:
                EER_title = "EERs"
                AUC_title = "AUCs"
            else:
                EER_title = "EER"
                AUC_title = "AUC"

            ###########################################################################################################
            ##################################### EER and scores section ##############################################
            ###########################################################################################################
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

            pdf.add_page()
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            pdf.image(self._fullname(outPath, first_name) + "_Genuine_Impostor_hist.png", ximg, None, wimg, himg)
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            if double_analysis is True:
                pdf.image(self._fullname(outPath, second_name) + "_Genuine_Impostor_hist.png", ximg, None, wimg, himg)
                pdf.add_page()
                y = pdf.get_y()
                pdf.set_xy(leftx, y + 5)
                pdf.image(self._fullname(outPath, "Genuine") + "_" + first_name + "_" + second_name + "_hist.png",
                          ximg, None, wimg, himg)
                y = pdf.get_y()
                pdf.set_xy(leftx, y + 5)
                pdf.image(self._fullname(outPath, "Impostor") + "_" + first_name + "_" + second_name + "_hist.png",
                          ximg, None, wimg, himg)

            pdf.add_page()
            pdf.multi_cell(0, cellh, "\n  Descriptive statistics in similarity scores", 1)
            pdf = self._report_scores_descriptive_statistics(pdf, first_desc_stats, first_name, xstart_double,
                                                             pdf.get_y(), tabw, tabh)
            if double_analysis is True:
                y = pdf.get_y()
                pdf = self._report_scores_descriptive_statistics(pdf, second_desc_stats, second_name, xstart_double,
                                                                 pdf.get_y(), tabw, tabh)

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

            ###########################################################################################################
            ##################################### Confusion matrix section ############################################
            ###########################################################################################################

            pdf.add_page()
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            pdf.set_font('Arial', '', cap)
            pdf.multi_cell(0, cellh, "\n Confusion Matrix\n", 1)
            pdf.set_font('Arial', '', text)
            pdf.multi_cell(0, cellh, "Confusion Matrix related to Genuines rate (G) and Impostors rate (I)", 0)
            y = pdf.get_y()
            pdf = self._report_confusion_matrix(pdf, first_cm, first_name, xstart_double, y, tabw, tabh)
            if double_analysis is True:
                y = pdf.get_y()
                pdf = self._report_confusion_matrix(pdf, second_cm, second_name, xstart_double, y, tabw, tabh)



            ###########################################################################################################
            ##################################### AUC and ROC curve section ###########################################
            ###########################################################################################################
            pdf.add_page()
            pdf.set_font('Arial', '', cap)
            pdf.multi_cell(0, cellh, "\n  AUC and ROC results", 1)
            pdf.set_font('Arial', '', text)
            y = pdf.get_y()
            pdf.set_xy(xstart, y+5)
            pdf.multi_cell(tabw * 2, tabh, AUC_title, border=1, align='C', fill=0)
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_xy(xstart, y)
            pdf.multi_cell(tabw, tabh, first_name, border=1, align='L', fill=0)
            pdf.set_xy(xstart + tabw, y)
            pdf.multi_cell(tabw, tabh, str(round(first_AUC, 5)), border=1, align='L', fill=0)
            if double_analysis is True:
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_xy(xstart, y)
                pdf.multi_cell(tabw, tabh, second_name, border=1, align='L', fill=0)
                pdf.set_xy(xstart + tabw, y)
                pdf.multi_cell(tabw, tabh, str(round(second_AUC, 5)), border=1, align='L', fill=0)

            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            pdf.image(self._fullname(outPath, first_name) + "_roc.png", ximg, None, wimg, himg)
            y = pdf.get_y()
            pdf.set_xy(leftx, y + 5)
            if double_analysis is True:
                pdf.image(self._fullname(outPath, second_name) + "_roc.png", ximg, None, wimg, himg)
                pdf.add_page()
                y = pdf.get_y()
                pdf.set_xy(leftx, y + 5)
                pdf.image(self._fullname(outPath, first_name) + "_" + second_name + "_roc.png", ximg, None, wimg, himg)
                pdf.add_page()
                y = pdf.get_y()
                pdf.set_xy(leftx, y + 5)

        ###############################################################################################################
        #################################### Statistical analysis section #############################################
        ###############################################################################################################
        if statistical_analysis is True or permutation_test is True:
            features_row = "            "
            if not(pvalues is None):
                features = len(pvalues)
            else:
                features = len(p_perm)
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
            pdf = self._report_statistical_analysis(pdf, pvalues, ds, xstart_double, pdf.get_y(), tabw, tabh)
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
            G, I, thr = biom.genuines_and_impostors(scores, first_labels)
            if not(threshold is None):
                thr = self._compute_thresholds(threshold)
            desc_stats = self._scores_descriptive_statistics(biom, G, I)
            FAR, FRR, CRR, CAR, EER, AUC = biom.compute_performance_analysis(G, I, thr)
            cm = biom.confusion_matrix(FAR, FRR)
            self._print_confusion_matrix(cm, name)

            if view_analysis is True or generate_pdf is True:
                EER_scores_results = "EER of the " + str(name) + " group: %.5f" % EER
                EER_scores_results += "\n\nGenuine and Impostor similarity scores distributions:"
                rates_results = "\n\nFalse Acceptance Rates and False Rejection Rates:"
                AUC_results = "AUC of the " + str(name) + " group: %.5f" % AUC

                if view_analysis is True:
                    print(EER_scores_results)
                    print("\nGenuine descriptive statistics:\n  Mean:   %.5f" % desc_stats['mean'][0])
                    print("\n  Median: %.5f" % desc_stats['median'][0])
                    print("\n  Std:    %.5f" % desc_stats['std'][0])
                    print("\nImpostor descriptive statistics:\n  Mean:   %.5f" % desc_stats['mean'][1])
                    print("\n  Median: %.5f" % desc_stats['median'][1])
                    print("\n  Std:    %.5f" % desc_stats['std'][1])
                self._scores_histogram(G, name, "Genuine", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(I, name, "Impostor", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram_comparison(G, I, name, "Genuine", "Impostor", bins, view_analysis, generate_pdf,
                                                  outPath)

                if view_analysis is True:
                    print(AUC_results)
                self._roc_curve(FAR, CAR, name, view_analysis, generate_pdf, outPath)

                if view_analysis is True:
                    print(rates_results)
                self._rates_plot(FAR, FRR, thr, name, view_analysis, generate_pdf, outPath)

        if generate_pdf is True:
            if not (".pdf" in report_name):
                report_name += ".pdf"
            self._report(biometric_analysis, False, False, name, None, EER, None, AUC, None, desc_stats, None, cm, None,
                         rates_results,None, None, None, None, None, None, None, None, None,
                         report_name, outPath, double_analysis=False)


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

        first, first_labels = data_manager.data_management(first_data, first_labels)
        second, second_labels = data_manager.data_management(second_data, second_labels)

        print(np.shape(first_data))
        if not(selection_algorithm is None or selected_features is None):
            first_data = features_selector.select_features(selection_algorithm,
                                                           first_data,
                                                           selected_features)
            second_data = features_selector.select_features(selection_algorithm,
                                                            second_data,
                                                            selected_features)

        if biometric_analysis is True:
            print('Computing genuine and impostor scores')
            first_scores = biom.compute_scores(first_data, distance)
            first_G, first_I, first_thr = biom.genuines_and_impostors(first_scores, first_labels)
            first_desc_stats = self._scores_descriptive_statistics(biom, first_G, first_I)

            second_scores = biom.compute_scores(second_data, distance)
            second_G, second_I, second_thr = biom.genuines_and_impostors(second_scores, second_labels)
            second_desc_stats = self._scores_descriptive_statistics(biom, second_G, second_I)

            if not(threshold is None):
                first_thr = self._compute_thresholds(threshold)
                second_thr = first_thr

            print('\nComputing biometric performance:\n First group:  ')
            first_FAR, first_FRR, first_CRR, first_CAR, first_EER, first_AUC = \
                biom.compute_performance_analysis(first_G, first_I, first_thr)
            print("\n Second group: ")
            second_FAR, second_FRR, second_CRR, second_CAR, second_EER, second_AUC = \
                biom.compute_performance_analysis(second_G, second_I, second_thr)
            print("")
            first_cm = biom.confusion_matrix(first_FAR, first_FRR)
            second_cm = biom.confusion_matrix(second_FAR, second_FRR)
            self._print_confusion_matrix(first_cm, first_name)
            self._print_confusion_matrix(second_cm, second_name)


            if statistical_analysis is True:
                print('\nComputing statistical analysis between scores')
                pvalue_G, d_G = statan.compute_scores_statistics(first_G, second_G)
                pvalue_I, d_I = statan.compute_scores_statistics(first_I, second_I)

        if permutation_test is True:
            print('Computing permutation test between features')
            p_perm = perm_test.compute_permutation_test(first, second, permutation_method,
                                                        permutation_assumption, permutation_repetitions, first_labels,
                                                        second_labels)

        if statistical_analysis is True:
            print('Computing statistical analysis between features')
            pvalue, d = statan.compute_features_statistics(first, second, first_labels, second_labels)

        if view_analysis is True or generate_pdf is True:
            if biometric_analysis is True:
                EER_scores_results = "EER of the " + str(first_name) + " group: %.5f" % first_EER
                EER_scores_results += "\n\n"
                EER_scores_results += "EER of the " + str(second_name) + " group: %.5f" % second_EER
                EER_scores_results += "\n\nGenuine and Impostor similarity scores distributions:"

                AUC_results = "AUC of the " + str(first_name) + " group: %.5f" % first_AUC
                AUC_results += "\n\n"
                AUC_results += "AUC of the " + str(second_name) + " group: %.5f" % second_AUC
                AUC_results += "\n\nReceiver Operating Characteristic curves:"

                rates_results = "\n\nFalse Acceptance Rates and False Rejection Rates:"
                if statistical_analysis is True:
                    genuine_statistical_results = "\n\nResults of the statistical analysis between the two Genuine scores:\n\n  - pvalue:    %.5f" % pvalue_G
                    genuine_statistical_results += "\n  - Cohen's d: %.5f" % d_G
                    impostor_statistical_results = "\n\nResults of the statistical analysis between the two Impostor scores:\n\n  - pvalue:    %.5f" % pvalue_I
                    impostor_statistical_results += "\n  - Cohen's d: %.5f" % d_I

            permutation_results, features_row, permutation_results_p = self._permutation_strings(permutation_test,
                                                                                                 first_name,
                                                                                                 second_name,
                                                                                                 p_perm)

            if biometric_analysis is True:
                if view_analysis is True:
                    print(EER_scores_results)
                    print("\n Descriptive statistics on scores: " + first_name)
                    print("\nGenuine descriptive statistics:\n  Mean:   %.5f" % first_desc_stats['mean'][0])
                    print("\n  Median: %.5f" % first_desc_stats['median'][0])
                    print("\n  Std:    %.5f" % first_desc_stats['std'][0])
                    print("\nImpostor descriptive statistics:\n  Mean:   %.5f" % first_desc_stats['mean'][1])
                    print("\n  Median: %.5f" % first_desc_stats['median'][1])
                    print("\n  Std:    %.5f" % first_desc_stats['std'][1])
                    print("\n Descriptive statistics on scores: " + second_name)
                    print("\nGenuine descriptive statistics:\n  Mean:   %.5f" % second_desc_stats['mean'][0])
                    print("\n  Median: %.5f" % second_desc_stats['median'][0])
                    print("\n  Std:    %.5f" % second_desc_stats['std'][0])
                    print("\nImpostor descriptive statistics:\n  Mean:   %.5f" % second_desc_stats['mean'][1])
                    print("\n  Median: %.5f" % second_desc_stats['median'][1])
                    print("\n  Std:    %.5f" % second_desc_stats['std'][1])
                self._scores_histogram(first_G, first_name, "Genuine", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(second_G, second_name, "Genuine", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(first_I, first_name, "Impostor", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram(second_I, second_name, "Impostor", bins, view_analysis, generate_pdf, outPath)
                self._scores_histogram_comparison(first_G, first_I, first_name, "Genuine", "Impostor", bins,
                                                  view_analysis, generate_pdf, outPath)
                self._scores_histogram_comparison(second_G, second_I, second_name, "Genuine", "Impostor", bins,
                                                  view_analysis, generate_pdf, outPath)
                self._scores_histogram_comparison(first_G, second_G, "Genuine", first_name, second_name, bins,
                                                  view_analysis, generate_pdf, outPath)
                self._scores_histogram_comparison(first_I, second_I, "Impostor", first_name, second_name, bins,
                                                  view_analysis, generate_pdf, outPath)
                if view_analysis is True:
                    print(AUC_results)
                self._roc_curve(first_FAR, first_CAR, first_name, view_analysis, generate_pdf, outPath)
                self._roc_curve(second_FAR, second_CAR, second_name, view_analysis, generate_pdf, outPath)
                self._roc_curve_comparison(first_FAR, first_CAR, second_FAR, second_CAR, first_name, second_name,
                                           view_analysis, generate_pdf, outPath)

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
                    print("P-values: ", end=" ")
                    print(pvalue)
                    print("Cohen's d:", end=" ")
                    print(d)
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
                self._report(biometric_analysis, statistical_analysis, permutation_test, first_name, second_name,
                             first_EER, second_EER, first_AUC, second_AUC, first_desc_stats, second_desc_stats,
                             first_cm, second_cm, rates_results, pvalue, d, pvalue_G, d_G, pvalue_I, d_I, p_perm,
                             permutation_results,permutation_results_p, report_name, outPath, double_analysis=True)


    def _statistical_strings(self, statistical_analysis, first_name, second_name, pvalue, d):
        """
        The _statistical_strings method is used for generating the strings related to the statistical analysis results
        between features (FOR INTERNAL USE ONLY).

        :param statistical_analysis: True if statistical analysis were computed, False otherwise
        :param first_name:           the name of the first group of data
        :param second_name:          the name of the second group of data
        :param pvalue:               the matrix representing the p-value for each feature
        :param d:                    the matrix representing the Cohen's d for each feature

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


    def _scores_descriptive_statistics(self, biom, genuine_scores, impostor_scores):
        """
        The _scores_secriptive_statistics method provides a dictionary containing all the descriptive statistics related
        the distributions of similarity scores, as 2-element lists containing the value related to the genuine scores as
        first element and the value related to the impostor scores as second element (FOR INTERNAL USE ONLY).

        :param biom:            is the biometric_performance object
        :param genuine_scores:  is the 1D-array representing the genuine scores distribution
        :param impostor_scores: is the 1D-array representing the impostor scores distribution

        :return:                a disctionary containing the descriptive statistics
        """
        stats = dict()
        G_mean, G_median, G_std = biom.scores_statistics(genuine_scores)
        I_mean, I_median, I_std = biom.scores_statistics(impostor_scores)
        stats['mean'] = [G_mean, I_mean]
        stats['median'] = [G_median, I_median]
        stats['std'] = [G_std, I_std]
        return stats


    def _print_confusion_matrix(self, cm, group_name=""):
        """
        The _print_confusion_matrix prints the confusion matrix (FOR INTERNAL USE ONLY).

        :param cm:         is the confusion matrix ([[CAR, FRR],[FAR, CRR]])
        :param group_name: is the name of the analyzed group ("" by default)
        """
        print("\nConfusion matrix of the " + group_name + "group:")
        print("        Predicted Genuine   Predicted Impostor")
        print("Genuine  %.5f" % cm[0][0], end="")
        print("   %.5f" % cm[0][1])
        print("Impostor %.5f" % cm[1][0], end="")
        print("   %.5f" % cm[1][1])