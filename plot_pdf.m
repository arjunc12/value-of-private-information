function [] = plot_pdf(offer_type)

  filename = ['data/' offer_type '_pdf'];
  pdf1 = load([filename '1']);
  pdf2 = load([filename '2']);

  interval = -10:0.001:19.999;

  h = figure;

  subplot(2, 3, [1 2]);
  plot(interval, pdf1', interval, normpdf(interval, 2, 1), 'LineWidth', 2);
  xlabel('Value');
  ylabel('Probability');
  title('Distribution for Private Type 1');

  subplot(2, 3, [4 5]);
  plot(interval, pdf2', interval, normpdf(interval, 7, 1), 'LineWidth', 2);
  xlabel('Value');
  ylabel('Probability');
  title('Distribution for Private Type 2');

  subplot(2, 3, [3 6]);
  p = plot(interval, pdf2', interval, normpdf(interval, 7, 1), 'LineWidth', 2);
  set(p, 'Visible', 'Off');
  legend('Learned', 'True', 'Location', 'West');
  axis off

  save2pdf('distribution.pdf', h, 600);

end
